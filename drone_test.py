from drone_api import DroneController
import time

token = '60ac081f527e8baab8ac3bae078d1922d34cfd2e' # personal access token
# token_api = 'NjEzZDA4MjI0YjIzYmM0NGJkNjU5ZDlhNzZkZDEzODk4MmYzNzE3OGFiZjc4OWZhMThhYzE5MjQ=' # api key

droneHandle = DroneController(Token=token, VehicleId='r4EeYcnz',
                              fb_server_url='https://dev.flytbase.com/rest/ros/flytos')

# print(droneHandle.get_links())

# print "#### FlytBase Cloud ####"


# print "sending takeoff command"
# print (droneHandle.take_off(1.0))

# print "Wait for some time"
# time.sleep(4.0)

# print "sending yaw rate command"
# print (droneHandle.velocity_set(0.0, 0.0, 0.0, yaw_rate=0.8, yaw_rate_valid=True))

# time.sleep(10.0)

# print "sending position hold command"
# print(droneHandle.position_hold()
# )
# print "sending land command"
# print (droneHandle.land(True))

# print droneHandle.position_hold()
# print droneHandle.position_set_global(37.429353, -122.083684, 5.0, 0.0, 1.0, False, False)
# print droneHandle.velocity_set(0.0, 0.0, 0.0)
# print droneHandle.rtl()
# print droneHandle.get_global_position()
# print droneHandle.get_battery_status()
# print droneHandle.get_local_position()