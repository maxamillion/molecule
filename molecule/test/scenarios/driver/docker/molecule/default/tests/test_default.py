import re
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_hostname(host):
    assert re.search(r'instance.*', host.check_output('hostname -s'))


def test_etc_molecule_directory(host):
    f = host.file('/etc/molecule')

    assert f.is_directory
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o755


def test_etc_molecule_ansible_hostname_file(host):
    f = host.file('/etc/molecule/{}'.format(host.check_output('hostname -s')))

    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644


def test_buildarg_env_var(host):
    cmd_out = host.run("echo $envarg")
    assert cmd_out.stdout.strip() == 'this_is_a_test'
