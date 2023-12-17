
# here are the  routers and permissions for read and write for different databases

class FinlandSwedenRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'finland_app':
            return 'finland'
        elif model._meta.app_label == 'sweden_app':
            return 'sweden'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'finland_app':
            return 'finland'
        elif model._meta.app_label == 'sweden_app':
            return 'sweden'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_set = {"default", "finland", "sweden"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    # ... other router methods ...
