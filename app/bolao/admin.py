from django.contrib import admin
from .models import Jogador
from .models import Partida
from .models import Aposta
from .models import Time
from .models import ResultadoAposta

admin.site.register(Jogador)
admin.site.register(Partida)
admin.site.register(Aposta)
admin.site.register(Time)
admin.site.register(ResultadoAposta)
