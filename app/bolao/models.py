from django.db import models

class Jogador(models.Model):
    login = models.CharField(max_length=100, primary_key=True)
    senha = models.CharField(max_length=100)
    nome = models.CharField(max_length=200)
    credito = models.DecimalField(default=10.0)

    class Meta:
        verbose_name = 'Jogador'
        verbose_name_plural = 'Jogadores'

    def __str__(self):
        return self.nome

class Time(models.Model):
    codigo = models.AutoField(primary_key=True)
    sigla = models.CharField(max_length=3)
    nome = models.CharField(max_length=200)
    bandeira = models.ImageField(upload_to='img/flags/', default='img/flags/no-flag.jpg')

    class Meta:
        verbose_name = 'Time'
        verbose_name_plural = 'Times'

    def __str__(self):
        return self.nome
    
class ResultadoAposta(models.Model):
    loginJogador = models.ForeignKey('Jogador', on_delete=models.CASCADE)
    codigoPartida = models.ForeignKey('Partida', on_delete=models.CASCADE)
    codigoAposta = models.ForeignKey('Aposta', on_delete=models.CASCADE)
    valorGanho = models.DecimalField(default=0.0)

    class Meta:
        verbose_name = 'Resultado da Aposta'
        verbose_name_plural = 'Resultados das Apostas'

class Partida(models.Model):
    codigo = models.AutoField(primary_key=True)
    timeA = models.ForeignKey('Time', on_delete=models.CASCADE)
    timeB = models.ForeignKey('Time', on_delete=models.CASCADE)
    golsTimeA = models.IntegerField(blank=True, null=True)
    golsTimeB = models.IntegerField(blank=True, null=True)
    data = models.DateTimeField(blank=False, null=False)

    class Meta:
        verbose_name = 'Partida'
        verbose_name_plural = 'Partidas'

    def atualizar(self):
        if not self.golsTimeA and not self.golsTimeB:
            apostas = Aposta.objects.filter(codigoPartida=codigo)
            
            vencedores = apostas.filter(apostaGolsTimeA=golsTimeA, apostaGolsTimeB=golsTimeB)
            
            if len(vencedores) == 0:
                for aposta in apostas:
                    jogador = Jogador.objects.get(login=aposta.loginJogadorAposta)
                    jogador.credito += aposta.valor
                    jogador.save()
            else:
                qtApostas = len(apostas)
                montante = sum([aposta.valor for aposta in apostas])
                for aposta in apostas:
                    jogador = Jogador.objects.get(login=aposta.loginJogadorAposta)
                    jogador.credito += (montante / qtApostas)
                    jogador.save()
                    
                    resultado = ResultadoAposta(loginJogador=aposta.loginJogadorAposta, \
                                                codigoPartida=aposta.codigoPartidaApostada, \
                                                codigoAposta=aposta.codigo, \
                                                valorGanho=(montante/qtApostas))
                    
                    resultado.save()

    def __str__(self):
        nomeA = Time.objects.get(codigo=timeA)
        nomeB = Time.objects.get(codigo=timeB)
        return nomeA.nome + ' x ' + nomeB.nome
    
class Aposta(models.Model):
    codigo = models.AutoField(primary_key=True)
    loginJogadorAposta = models.ForeignKey('Jogador', on_delete=models.CASCADE)
    codigoPartidaApostada = models.ForeignKey('Partida', on_delete=models.CASCADE)
    valor = models.DecimalField(default=5.0) # por mais que seja 5 fixo, é melhor criar esse campo
    apostaGolsTimeA = models.IntegerField(blank=False, null=False)
    apostaGolsTimeB = models.IntegerField(blank=False, null=False)

    class Meta:
        verbose_name = 'Aposta'
        verbose_name_plural = 'Apostas'

    def __str__(self):
        partida = Partida.objects.get(codigo=codigoPartida)
        return self.loginJogador + ' - ' + str(partida) + ' - ' + valor
