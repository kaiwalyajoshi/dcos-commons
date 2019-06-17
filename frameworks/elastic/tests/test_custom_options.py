from tests import config
import pytest
import sdk_cmd
import sdk_install
import sdk_tasks
import logging

log = logging.getLogger(__name__)


@pytest.mark.sanity
def test_xmx_and_xms_flags(configure_security):
    """ method to test the duplication of JVM flags in elastic tasks """

    # setting custom values for the heap of various pods
    MASTER_NODE_HEAP = 700
    DATA_NODE_HEAP = 800
    COORDINATOR_NODE_HEAP = 900
    INGEST_NODE_HEAP = 1000

    sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)
    # installing elastic service and passing customized json to overwrite default values.
    sdk_install.install(
        config.PACKAGE_NAME,
        config.SERVICE_NAME,
        config.DEFAULT_TASK_COUNT,
        {
            "master_nodes": {"heap": {"size": MASTER_NODE_HEAP}},
            "data_nodes": {"heap": {"size": DATA_NODE_HEAP}},
            "coordinator_nodes": {"heap": {"size": COORDINATOR_NODE_HEAP}},
            "ingest_nodes": {"heap": {"size": INGEST_NODE_HEAP}},
        },
    )
    # getting all the tasks and checking the flag duplicacy by running curl_cmd command.
    for task in sdk_tasks.get_task_ids(config.SERVICE_NAME):
        cmd = "ps aux"
        flag_xms = "Xms"
        flag_xmx = "Xmx"
        exit_code, stdout, stderr = sdk_cmd.service_task_exec(config.SERVICE_NAME, task, cmd)

        assert str(stdout).count(flag_xms) == 1, "Default xms flag prefix should appear once"

        assert str(stdout).count(flag_xmx) == 1, "Default xmx flag prefix should appear once"

        if str(task).count("master"):
            master_xms = flag_xms + str(MASTER_NODE_HEAP)
            master_xmx = flag_xmx + str(MASTER_NODE_HEAP)
            log.info("Checking flags in master node: " + task)
            assert (
                str(stdout).count(master_xms) == 1
            ), "Configured master node xms flag prefix should appear once"
            assert (
                str(stdout).count(master_xmx) == 1
            ), "Configured master node xmx flag prefix should appear once"

        if str(task).count("data"):
            data_xms = flag_xms + str(DATA_NODE_HEAP)
            data_xmx = flag_xmx + str(DATA_NODE_HEAP)
            log.info("Checking flags in data node: " + task)
            assert (
                str(stdout).count(data_xms) == 1
            ), "Configured data node xms flag prefix should appear once"
            assert (
                str(stdout).count(data_xmx) == 1
            ), "Configured data node xmx flag prefix should appear once"

        if str(task).count("coordinator"):
            coordinator_xms = flag_xms + str(COORDINATOR_NODE_HEAP)
            coordinator_xmx = flag_xmx + str(COORDINATOR_NODE_HEAP)
            log.info("Checking flags in coordinator node: " + task)
            assert (
                str(stdout).count(coordinator_xms) == 1
            ), "Configured coordinator node xms flag prefix should appear once"
            assert (
                str(stdout).count(coordinator_xmx) == 1
            ), "Configured coordinator node xmx flag prefix should appear once"

        if str(task).count("ingest"):
            ingest_xms = flag_xms + str(INGEST_NODE_HEAP)
            ingest_xmx = flag_xmx + str(INGEST_NODE_HEAP)
            log.info("Checking flags in ingest node: " + task)
            assert (
                str(stdout).count(ingest_xms) == 1
            ), "Configured ingest node flag xms prefix should appear once"
            assert (
                str(stdout).count(ingest_xmx) == 1
            ), "Configured ingest node flag xmx prefix should appear once"

    # uninstalling the installed service
    sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)
