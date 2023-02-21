import logging


class Logger:

    @classmethod
    def trace(cls, *dargs, **dkwargs):
        # logging.debug(f"--> Decor args: {dargs}")
        # logging.debug(f"--> Decor kwargs: {dkwargs}")
        def inner(func):
            def wrap(*args,**kwargs):
                # logging.debug(f"--> Running func: {func}")
                (f"--> Function args: {args}")
                logging.info(f"--> Function kwargs: {kwargs}")
                result = func(*args, **kwargs)
                logging.info(f"--> Function result: {result}")

                return result
            return wrap
        return inner

# @Logger.trace()
# def fun():
#     logging.debug("==> Actual fun")
#     return 42
