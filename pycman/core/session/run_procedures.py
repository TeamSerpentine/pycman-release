from copy import deepcopy
from multiprocessing import Pool


def _run_single(agents, env):
    agents[0].run(env.get())
    env.get().close()


def _run_sequential(agents, env):
    envs = [deepcopy(env.get()) for _ in agents]

    for agent, env in zip(agents, envs):
        agent.run(env)
        env.close()


def _run_parallel(agents, env):
    envs = [deepcopy(env.get()) for _ in agents]

    args = []
    for agent, env in zip(agents, envs):
        args.append((agent, env))
        # FIXME: create test case -> print(str(agent) + "##############")

    with Pool(len(agents)) as p:
        result = p.map(_start_worker, args)
        p.close()

    print(agents)
    for idx, a in enumerate(result):
        agents[idx] = a
    return


def _start_worker(info):
    info[0].part_of_parallel_pool = True
    info[0].run(info[1])
    info[1].close()
    info[0].parallel_logger_close()
    info[0].part_of_parallel_pool = False
    return info[0]
