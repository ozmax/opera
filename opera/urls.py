from django.conf.urls import url, include
from django.contrib import admin

import virtuoso.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^virtuoso/', include(virtuoso.urls)),
]
