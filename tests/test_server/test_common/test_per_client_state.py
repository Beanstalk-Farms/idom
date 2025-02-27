import pytest

import idom
from idom.server import fastapi as idom_fastapi
from idom.server import flask as idom_flask
from idom.server import sanic as idom_sanic
from idom.server import tornado as idom_tornado
from idom.testing import ServerMountPoint


@pytest.fixture(
    params=[
        # add new PerClientStateServer implementations here to
        # run a suite of tests which check basic functionality
        idom_sanic.PerClientStateServer,
        idom_flask.PerClientStateServer,
        idom_tornado.PerClientStateServer,
        idom_fastapi.PerClientStateServer,
    ],
    ids=lambda cls: f"{cls.__module__}.{cls.__name__}",
)
def server_mount_point(request):
    with ServerMountPoint(request.param) as mount_point:
        yield mount_point


def test_display_simple_hello_world(driver, display):
    @idom.component
    def Hello():
        return idom.html.p({"id": "hello"}, ["Hello World"])

    display(Hello)

    assert driver.find_element_by_id("hello")

    # test that we can reconnect succefully
    driver.refresh()

    assert driver.find_element_by_id("hello")


def test_display_simple_click_counter(driver, display):
    def increment(count):
        return count + 1

    @idom.component
    def Counter():
        count, set_count = idom.hooks.use_state(0)
        return idom.html.button(
            {
                "id": "counter",
                "onClick": lambda event: set_count(increment),
            },
            f"Count: {count}",
        )

    display(Counter)

    client_counter = driver.find_element_by_id("counter")

    for i in range(3):
        assert client_counter.get_attribute("innerHTML") == f"Count: {i}"
        client_counter.click()


def test_installed_module(driver, display):
    victory = idom.install("victory@35.4.0")
    display(victory.VictoryBar)
    driver.find_element_by_class_name("VictoryContainer")
