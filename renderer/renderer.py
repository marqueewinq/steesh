import fire
def renderer():
    return fire.Fire(lambda cardlist, output: (cardlist, output))