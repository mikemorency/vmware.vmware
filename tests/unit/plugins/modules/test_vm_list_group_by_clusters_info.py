from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys
import pytest

from ansible_collections.vmware.vmware.plugins.modules import vm_list_group_by_clusters_info

from ...common.utils import (
    run_module, ModuleTestCase
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestVMList(ModuleTestCase):

    def __prepare(self, mocker):
        init_mock = mocker.patch.object(vm_list_group_by_clusters_info.VmwareVMList, "__init__")
        init_mock.return_value = None

        vm_list_group_by_clusters_info.VmwareVMList.content = mocker.Mock()
        vm_list_group_by_clusters_info.VmwareVMList.module = mocker.Mock()
        vm_list_group_by_clusters_info.VmwareVMList.module.check_mode = False

        vm_list_group_by_clusters_info.VmwareVMList.params = {
            'detailed_vms': False,
        }

        list_of_vms = mocker.patch.object(vm_list_group_by_clusters_info.VmwareVMList, "get_vm_list_group_by_clusters")
        list_of_vms.return_value = {}

    def test_gather(self, mocker):
        self.__prepare(mocker)

        result = run_module(module_entry=vm_list_group_by_clusters_info.main, module_args={})
        assert result["changed"] is False
