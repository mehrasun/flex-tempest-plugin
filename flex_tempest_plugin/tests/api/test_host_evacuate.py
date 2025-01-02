# Yet to write copywrite thing

import time
from tempest.api.compute import base
from tempest.lib import decorators
from tempest import config
from tempest.lib.common.utils import data_utils

CONF = config.CONF


class HostEvacuateTestJSON(base.BaseV2ComputeAdminTest):
    """Tests Host Evacuate API.

    It spins a server on specific compute and then put it
    down to perform server evacuation and finally enable the host again.
    """

    create_default_network = True

    @classmethod
    def setup_clients(cls):
        super(HostEvacuateTestJSON, cls).setup_clients()
        cls.client = cls.os_admin.services_client
        cls.host_client = cls.os_admin.hosts_client
        cls.servers_client = cls.os_admin.servers_client

    @classmethod
    def resource_setup(cls):
        super(HostEvacuateTestJSON, cls).resource_setup()
        prefix = CONF.resource_name_prefix
        cls.s1_name = data_utils.rand_name(prefix=prefix,
                                           name=cls.__name__ + '-server')

    @decorators.idempotent_id('2d16d8cf-8ee7-4755-bd16-f18a834fff89')
    def test_host_evacuation(self):
        """
        (This should only be done on staging)
        Test host server evacuation
        """
        server = self.create_test_server(wait_until='ACTIVE')
        server_details = self.servers_client.show_server(server["id"])
        host_name = server_details["server"]["OS-EXT-SRV-ATTR:host"]
        services = self.client.list_services(host=host_name)['services']
        svc = [svc for svc in services if svc['host'] == host_name][0]
        self.client.update_service(svc["id"], forced_down=True)
        self.servers_client.evacuate_server(server["id"])

        status, after_evac_details, counter = None, None, 0
        while status != "ACTIVE" and counter < 60:
            time.sleep(1)
            after_evac_details = self.servers_client.show_server(server["id"])
            status = after_evac_details["server"]["status"]
            counter += 1
        self.assertNotEqual(host_name,
                            after_evac_details["server"]["OS-EXT-SRV-ATTR:host"])
        self.servers_client.delete_server(server["id"])
        self.client.update_service(svc["id"], status="enabled", forced_down=False)
