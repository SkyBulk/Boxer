from django import forms
from django_summernote.widgets import SummernoteWidget
from socket import if_nameindex
from netaddr import IPAddress, IPNetwork
from netaddr.core import AddrFormatError


class MailComposeForm(forms.Form):
    receiver = forms.CharField(max_length=255)
    subject = forms.CharField(max_length=255)
    content = forms.CharField(widget=SummernoteWidget())


class NewsForm(forms.Form):
    subject = forms.CharField(max_length=255)
    content = forms.CharField(widget=SummernoteWidget())


class NatForm(forms.Form):

    network_name = forms.CharField(max_length=255, label="Network name")
    bridge_name = forms.CharField(max_length=255, label="Bridge name")
    ip_network = forms.CharField(max_length=255, label="Network CIDR")
    host_ip = forms.CharField(
        max_length=255, label="Host assigned IP in new network"
    )
    dhcp_start = forms.CharField(max_length=255, label="DHCP starting IP")
    dhcp_end = forms.CharField(max_length=255, label="DHCP ending IP")
    interface = forms.ChoiceField(label="Gateway interface")

    def __init__(self, *args, **kwargs):
        nonexist = ("non-exising", "Select..")
        if kwargs.get('interfaces'):
            interfaces = kwargs.pop('interfaces')
            interfaces.append(nonexist)
        else:
            interfaces = []
        super().__init__(*args, **kwargs)
        self.fields['interface'].choices = interfaces
        self.fields['interface'].initial = nonexist
        self.fields['network_name'].initial = "alpha-nat"
        self.fields['bridge_name'].initial = "vibr1000"
        self.fields['ip_network'].initial = "10.10.10.10/24"
        self.fields['host_ip'].initial = "10.10.10.1"
        self.fields['dhcp_start'].initial = "10.10.10.10"
        self.fields['dhcp_end'].initial = "10.10.10.254"

    def clean(self):
        self.cleaned_data = super().clean()

        interface = self.cleaned_data.get("interface")

        ip_network = self.cleaned_data.get("ip_network")
        host_ip = self.cleaned_data.get("host_ip")
        dhcp_start = self.cleaned_data.get("dhcp_start")
        dhcp_end = self.cleaned_data.get("dhcp_end")

        int_check = False

        try:
            if int(interface):
                int_check = True
        except ValueError:
            self.add_error(
                'interface', "Interface does not seem to exist in the OS."
            )

        if int_check \
                and int(interface) not in range(1, len(if_nameindex()) + 1):
            self.add_error(
                'interface', "Interface does not seem to exist in the OS."
            )

        try:
            ip_network_clean = IPNetwork(ip_network)
        except AddrFormatError:
            self.add_error(
                'ip_network', "This is not a valid IP network range."
            )

        try:
            host_ip_clean = IPAddress(host_ip)
        except AddrFormatError:
            self.add_error('host_ip', "This is not a valid IP address.")

        try:
            dhcp_start_clean = IPAddress(dhcp_start)
        except AddrFormatError:
            self.add_error('dhcp_start', "This is not a valid IP address.")

        try:
            dhcp_end_clean = IPAddress(dhcp_end)
        except AddrFormatError:
            self.add_error('dhcp_end', "This is not a valid IP address.")

        if dhcp_start_clean not in ip_network_clean:
            self.add_error(
                'dhcp_start', "This IP does not belong to given network."
            )

        if dhcp_end_clean not in ip_network_clean:
            self.add_error(
                'dhcp_end', "This IP does not belong to given network."
            )

        if dhcp_end_clean <= dhcp_start_clean:
            self.add_error(
                'dhcp_end', "This IP cannot be below the starting one."
            )

        if dhcp_start_clean in [
                ip_network_clean.network, ip_network_clean.broadcast,
                host_ip_clean]:
            self.add_error(
                'dhcp_start',
                (
                    "This IP cannot be a network or "
                    "broadcast address of the network "
                    "as well as host assigned IP."
                )
            )

        if dhcp_end_clean in [
                ip_network_clean.network, ip_network_clean.broadcast,
                host_ip_clean]:
            self.add_error(
                'dhcp_end',
                (
                    "This IP cannot be a network or "
                    "broadcast address of the network "
                    "as well as host assigned IP."
                )
            )
