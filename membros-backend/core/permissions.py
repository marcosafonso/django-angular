from rest_framework import permissions

class CafePermission(permissions.BasePermission):
    """
    Permissao customizada. Usuario precisa da permissao core.add_teste(eu criei) pra acessar
    """
    def has_permission(self, request, view):

        if request.user.has_perm('core.add_teste'):
            return True
        
        return False

        # ip_addr = request.META['REMOTE_ADDR']
        # blacklisted = Blacklist.objects.filter(ip_addr=ip_addr).exists()
        # return not blacklisted
