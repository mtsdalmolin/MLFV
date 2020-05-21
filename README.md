# MLFV 2.0
MLFV é um projeto desenvolvido por alunos e professores da UFSM com o propósito de implementar um orquestrador de funções em cadeia. A sigla vem de **Machine Learning Function Virtualization**.
A primeira versão foi implementada e apresentada como Trabalho de Conclusão de Curso (TCC) do Renan, iniciando o projeto.
A segunda versão, cujo projeto se encontra, foi a abordagem de colocar toda a implementação em containers, com o propósito de distribuir as tarefas realizadas na cadeia. Essa proposta foi tema do TCC do Lucas.
No estado atual, estamos desenvolvendo a funcionalidade de fazer o processamento das tarefas na GPU.

## Pré-requisitos de Instalação
- [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [Python](https://python.org)

### Execução
- **sudo python server_deamon.py** localizado em: ../MLFV_2.0/comunication/servidor_dados
- **python MLFV_Module.py** localizado em: ../MLFV_2.0/MLFV
- **sudo python init.py** localizado em: ../MLFV_2.0/comunication/workers
- **python test_MLFV.py 01mb.csv** localizado em: ../MLFV_2.0/comunication/cliente

(Obs.: É necessário executar nas respectivas pastas dos arquivos, pois os caminhos estão configurados como relativos)

### Descrição dos arquivos
**server_deamon.py** é o servidor de descoberta dos workers, para que esses possam baixar os arquivos do MLFV e também descobrir onde está o servidor. O arquivo enviado é o **MLFV_docker.zip** que está na mesma pasta, o zip contém o **Dockerfile** e a pasta com os arquivos do MLFV. Se modificar algo no MLFV ou no **Dockerfile** tem que zipar os dois e alterar o **MLFV_docker.zip**

**MLFV_Module.py** é o módulo de recebimento de inscrições e pacotes do MLFV. Esse deve estar ativo para que os workers consigam se inscrever após o download e instanciação do docker.

**/workers/init.py** executa a instanciação dos workers que realizarão a inscrição no servidor, se disponibilizando a receber tarefas. (É possível levantar N workers).

Obs.: Na primeira vez todos os arquivos serão baixados e criados, após isso, para não ficar repetindo todo o processo pode ser executado o comando: sudo python2 init.py 0
Assim, o docker não será construído, apenas inicializado.

**test_MLFV.py** executa o teste no servidor, recebendo parâmetros do arquivo de entrada e/ou parâmetro de paralelização (ver no código como os parâmetros funcionam).

# MLFV 3.0
TODO: Integrar processamento na GPU com os containers disponibilizados pela nvidia ou tensorflow que já tem essa feature implementada.
TODO: Refatorar e organizar o código.

## Autores
- [Renan Lirio Souza](https://github.com/S0uzaR)
- [Lucas Micol](https://github.com/LMicol)
- [Matheus Dalmolin](https://github.com/mtsdalmolin)
- Prof. Dr. Celio Trois
