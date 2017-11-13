domain_name = data.get('domain_name')
service_name = data.get('service_name')
data_details = data.get('data_details')
delay_seconds = data.get('delay_seconds')
loop_count = data.get('loop_count')

if (int(delay_seconds) > 2):
	delay_seconds = 2

index = 0
while (int(index) < int(loop_count)):
    hass.services.call(domain_name, service_name, service_data=data_details, blocking=False)
    time.sleep(int(delay_seconds))
    index = index + 1
