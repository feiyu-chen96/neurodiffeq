import torch
import random
from neurodiffeq.conditions import NoCondition
from neurodiffeq.conditions import IVP
from neurodiffeq.networks import FCNN
from neurodiffeq.neurodiffeq import diff

N_SAMPLES = 10
ones = torch.ones(N_SAMPLES, 1, requires_grad=True)

x0, x1 = random.random(), random.random()
y0, y1 = random.random(), random.random()


def test_no_condition():
    N_INPUTS = 5
    N_OUTPUTS = 5

    for n_in, n_out in zip(range(1, N_INPUTS), range(1, N_OUTPUTS)):
        xs = [torch.rand(N_SAMPLES, 1, requires_grad=True) for _ in range(n_in)]
        net = FCNN(n_in, n_out)

        cond = NoCondition()
        y_cond = cond.enforce(net, *xs)
        y_raw = net(torch.cat(xs, dim=1))
        assert (y_cond == y_raw).all()


def test_ivp():
    x = x0 * ones
    net = FCNN(1, 1)

    cond = IVP(x0, y0)
    y = cond.enforce(net, x)
    assert (y == y0).all(), "y(0) != y_0"

    cond = IVP(x0, y0, y1)
    y = cond.enforce(net, x)
    assert (y == y0).all(), "y(0) != y_0"
    assert (diff(y, x) == y1).all(), "y'(0) != y'_0"
