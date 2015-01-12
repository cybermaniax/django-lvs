'''
Created on 9 sty 2015

@author: ghalajko
'''

from django import forms
from django.core.validators  import validate_ipv46_address
from ipvsstat.lvs import ipvs

class MySelect(forms.Select):
   
    def render_option(self, selected_choices, option_value, option_label):
        new_label = "%s - %s" %(option_value,option_label)
        return super(MySelect,self).render_option(selected_choices, option_value, new_label)


class VirtualServerForm(forms.Form):
    __VS_MODE = (
        ('TCP', 'TCP'),
        ('UDP', 'UDP'),
        ('FWM', 'Firewall-mark'),
    )
    
    _VS_SCHEDULER = (
        ('rr', 'Robin Robin'),
        ('wrr', 'Weighted Round Robin'),
        ('lc', 'Least-Connection'),
        ('wlc', 'Weighted Least-Connection'),
        ('lblc', 'Locality-Based Least-Connection'),
        ('lblcr', 'Locality-Based Least-Connection with Replication'),
        ('dh', 'Destination Hashing'),
        ('sh', 'Source Hashing'),
        ('sed', 'Shortest Expected Delay'),
        ('nq', 'Never Queue'),
    )
    
    ip = forms.CharField(label='Ip Address', max_length=100,required=False,validators=[validate_ipv46_address],
                         widget=forms.TextInput(attrs={'class':'form-control','placeholder':'192.168.1.1'}))
    
    port = forms.IntegerField(label='Port',required=False,
                           min_value=0,
                           max_value=65535,
                           widget=forms.TextInput(attrs={'class':'form-control'}))
    
    fwmark = forms.IntegerField(label='Firewall-mark',required=False,
                           min_value=1,
                           widget=forms.TextInput(attrs={'class':'form-control'}))
    
    peristtimeout = forms.IntegerField(label='Persistent timeout (seconds)',required=False,
                           min_value=0,
                           widget=forms.TextInput(attrs={'class':'form-control'}))
    
    type = forms.ChoiceField(choices=__VS_MODE,initial='TCP', required=True, label="Select virtual server type",
                             widget=forms.RadioSelect)
    
    scheduler = forms.ChoiceField(choices=_VS_SCHEDULER, required=True, label="Scheduling-method",
                                  widget=MySelect(attrs={'class':'form-control'}))
    
    def clean(self):
        cleaned_data = super(VirtualServerForm, self).clean()
        v_type = cleaned_data.get('type')
        if 'TCP' in v_type or 'UDP' in v_type:
            v_ip = cleaned_data.get('ip')
            v_port = cleaned_data.get('port')
            if not v_ip:
                self.add_error('ip', 'This field is required.')
            if not v_port:
                self.add_error('port', 'This field is required.')
                
            if ipvs.isExist_virtual_server('%s:%s'%(v_ip,v_port)):
                self.add_error('ip', 'Ip address and port exist')
            
        elif 'FWM' in v_type:
            v_fwmark = cleaned_data.get('fwmark')
            if not v_fwmark:
                self.add_error('fwmark', 'This field is required.')
            if ipvs.isExist_virtual_server(str(v_fwmark)):
                self.add_error('fwmark', 'Virtual server with this firewall mark exist.')
        else:
            raise forms.ValidationError("No supported vs type"
                        "No supported vs type")
        
    