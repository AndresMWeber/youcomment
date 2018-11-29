from six import iteritems
import os
from youcomment.errors import EnvironmentError, ConfigError
from youcomment.conf import LOG
from functools import wraps


class BotMixin(object):
    ENV_VAR_DEPENDENCIES = {}


def ensure_instance_env_var_dependencies(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        for k, v in iteritems(self.ENV_VAR_DEPENDENCIES):
            if not os.getenv(k):
                LOG.debug('Cannot instantiate {CLS} without env var {ENV}'.format(CLS=self, ENV=k))
                raise EnvironmentError('Environment variable not set: %s' % k)

            elif not v:
                LOG.debug('Cannot instantiate {CLS} without config var {ENV}'.format(CLS=self, ENV=k))
                raise ConfigError('Environment variable not set: %s' % k)
            else:
                LOG.debug('Config/Env Var %s found.' % k)
        fn(self, *args, **kwargs)

    return wrapper
