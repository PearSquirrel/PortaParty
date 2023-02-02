import json
from requests import get, put, post


class DroneController(object):
    def __init__(self, Token=None, VehicleId=None, fb_server_url='', local=False):
        # replace with your own drone
        self.local = local
        if self.local:
            self.headers = {}
        else:
            self.headers = {'Authorization': 'Token ' + Token, 'VehicleID': VehicleId, 'namespace': 'flytos'}
        self.fb_server_url = fb_server_url

    def get_links(self):
        res = post('http://dev.flytbase.com:80' + '/list_streams', headers=self.headers)
        if res.status_code == 200:
            resp = res.json()
            success = resp["success"]
            msg = resp["message"]
            return (success, msg)
        else:
            return (False, "request failed")

    def take_off(self, takeoff_alt=1.0):
        '''
        Takeoff routine for the vehicle. Takes height as argument according to NED convention.
        '''
        res = post(self.fb_server_url + '/navigation/takeoff', headers=self.headers,
                  data=json.dumps({"takeoff_alt": takeoff_alt}))
        if res.status_code == 200:
            resp = res.json()
            success = resp["success"]
            msg = resp["message"]
            print (res, res.headers, res.url, res.content, res.reason, res.request)

            return (success, msg)
        else:
            print (res, res.headers, res.url, res.content, res.reason, res.request)
            print("take off...")
            # print (res.content)
            return (False, "request failed")

    def land(self, async_param=True):
        '''
        Land the vehicle. Function take no arguments.
        '''
        res = post(self.fb_server_url + '/navigation/land', headers=self.headers,
                  data=json.dumps({"async": async_param}))
        if res.status_code == 200:
            resp = res.json()
            success = resp["success"]
            msg = resp["message"]
            return (success, msg)
        else:
            print (res)
            return (False, "request failed")

    def position_hold(self):
        '''
        Land the vehicle. Function take no arguments.
        '''
        res = post(self.fb_server_url + '/navigation/position_hold', headers=self.headers)
        if res.status_code == 200:
            resp = res.json()
            success = resp["success"]
            msg = resp["message"]
            return (success, msg)
        else:
            return (False, "request failed")

    def position_set_global(self, lat, lon, rel_ht, yaw=0.0, tolerance=0.0, async_param=False, yaw_valid=False):
        '''
        Land the vehicle. Function take no arguments.
        '''
        res = post(self.fb_server_url + '/navigation/position_set_global', headers=self.headers,
                  data=json.dumps({'lat_x': lat, 'long_y': lon, 'rel_alt_z': rel_ht, 'yaw': yaw,
                                   'tolerance': tolerance, 'async': async_param,
                                   'yaw_valid': yaw_valid}))
        if res.status_code == 200:
            resp = res.json()
            success = resp["success"]
            msg = resp["message"]
            return (success, msg)
        else:
            print (res)
            return (False, "request failed")

    def velocity_set(self, vx, vy, vz, yaw_rate=0.0,
                     tolerance=1.0, relative=False, async_param=True, yaw_rate_valid=False, body_frame=True):
        res = post(self.fb_server_url + '/navigation/velocity_set', headers=self.headers,
                  data=json.dumps({"vx": vx, "vy": vy, "vz": vz, "yaw_rate": yaw_rate,
                                   "tolerance": tolerance, "async": async_param, "relative": relative,
                                   "yaw_rate_valid": yaw_rate_valid, "body_frame": body_frame}))
        if res.status_code == 200:
            resp = res.json()
            success = resp["success"]
            msg = resp["message"]
            return (success, msg)
        else:
            print (res)
            return (False, "request failed")

    def rtl(self):
        '''return to home, altitude will rise to 15 meters to avoid obstacles.
        Make sure that there are no obstacles
        '''
        res = get(self.fb_server_url + '/navigation/rtl', headers=self.headers)
        if res.status_code == 200:
            resp = res.json()
            success = resp["success"]
            msg = resp["message"]
            return (success, msg)
        else:
            return (False, "request failed")

    def get_global_position(self):
        res = get(self.fb_server_url + '/mavros/global_position/global', headers=self.headers)
        if res.status_code == 200:
            resp = res.json()
            return ({'longitude': resp['longitude'], 'latitude': resp['latitude'], 'altitude': resp['altitude'], })
        else:
            return (False, "request failed")

    def get_battery_status(self):
        res = get(self.fb_server_url + '/mavros/battery', headers=self.headers)
        if res.status_code == 200:
            resp = res.json()
            return {'voltage': resp['voltage'], 'current': resp['current'], 'remaining': 0.0}
        else:
            return (False, "request failed")

    def get_local_position(self):
        res = get(self.fb_server_url + '/mavros/local_position/local', headers=self.headers)
        if res.status_code == 200:
            resp = res.json()
            return True
        else:
            return (False, "request failed")

    def get_vehicle_state(self):
        res = get(self.fb_server_url + '/flyt/state', headers=self.headers)
        if res.status_code == 200:
            resp = res.json()
            return True
        else:
            return (False, "request failed")
