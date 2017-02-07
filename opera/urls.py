from django.conf.urls import url, include
from django.contrib import admin

import virtuoso.urls
import trends.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include(virtuoso.urls)),
    url(r'^trends/', include(trends.urls)),
]
