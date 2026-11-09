from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """
    Permission class untuk Tutorial 07 (Project):
    - SAFE_METHODS (GET, HEAD, OPTIONS): diizinkan untuk semua (termasuk pengunjung).
    - Metode tulis/ubah/hapus: hanya diizinkan untuk pemilik portofolio (superuser).
    """

    message = "Hanya pemilik portofolio yang memiliki hak akses untuk tindakan ini."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.is_superuser)


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Permission class untuk Tugas 6 (Education):
    - Pengunjung tanpa login: hanya boleh membaca (SAFE_METHODS).
    - Pengguna biasa: hanya boleh membaca (SAFE_METHODS). Pemberian star diatur terpisah.
    - Editor: boleh membaca dan mengubah data (PUT, PATCH), dilarang menambah (POST) atau menghapus (DELETE).
    - Pemilik portofolio (superuser): memiliki hak penuh (GET, POST, PUT, PATCH, DELETE).
    """

    message = "Anda tidak memiliki hak akses yang memadai untuk tindakan ini."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user or not user.is_authenticated:
            return False

        if request.method in ("PUT", "PATCH"):
            is_editor = user.groups.filter(name="Editor").exists()
            return user.is_superuser or is_editor

        if request.method in ("POST", "DELETE"):
            return user.is_superuser

        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

