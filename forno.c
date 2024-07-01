#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include <pthread.h>

#define MAX_PLACAS 100

typedef struct {
    int numero;
    bool stuck;
    time_t entrada;
    int tempo_espera;
    bool aviso_emperrado;
} Placa;

Placa placas[MAX_PLACAS];
int contador = 0;
int tempo_saida = 5;
int inputAsAnInteger;
bool running = true;

pthread_mutex_t lock;  //Uma estrutura pthread_mutex_t é usada para bloquear/desbloquear threads(tarefa de um programa de computador)

void adicionar_placa(int tempo_saida) {
    pthread_mutex_lock(&lock);

    if (contador >= MAX_PLACAS) {
        printf("Maximo de placas atingido.\n");
        pthread_mutex_unlock(&lock); 
        return;
    }

    time_t agora = time(NULL);
    contador++;
    
    Placa nova_placa;
    nova_placa.numero = contador;
    nova_placa.stuck = false;
    nova_placa.entrada = agora;
    nova_placa.tempo_espera = 0;
    nova_placa.aviso_emperrado = false;

    if (contador > 1) {
        Placa ultima_placa = placas[contador - 2];
        nova_placa.tempo_espera = (int)difftime(agora, ultima_placa.entrada);
    } else {
        nova_placa.tempo_espera = tempo_saida;
    }

    placas[contador - 1] = nova_placa;

    printf("Placa %d entrou\n", nova_placa.numero);
    
    pthread_mutex_unlock(&lock);
}

void saida(int tempo_saida) {
    while (running) {
        pthread_mutex_lock(&lock);

        time_t agora = time(NULL);

        for (int i = 0; i < contador; i++) {
            Placa *placa_info = &placas[i];
            int tempo_desde_entrada = (int)difftime(agora, placa_info->entrada);
            int tempo_esperado_saida;

            if (i == 0) {
                tempo_esperado_saida = tempo_saida;
            } else {
                Placa *placa_anterior = &placas[i - 1];
                if (placa_anterior->stuck) {
                    break;
                }
                tempo_esperado_saida = placa_anterior->tempo_espera + tempo_saida;
            }
            if (tempo_desde_entrada >= tempo_esperado_saida) {
                if (!placa_info->stuck) {
                    printf("Placa %d saiu\n", placa_info->numero);
                    for (int j = i; j < contador - 1; j++) {
                        placas[j] = placas[j + 1];
                    }
                    contador--;
                    break;
                } else if (!placa_info->aviso_emperrado) {
                    printf("Placa %d nao foi detectada como saida apos o tempo de espera!\n", placa_info->numero);
                    placa_info->aviso_emperrado = true;
                }
            }
        }
        pthread_mutex_unlock(&lock);
    }
}

void simular_emperramento(int placa_num) {
    pthread_mutex_lock(&lock);

    for (int i = 0; i < contador; i++) {
        if (placas[i].numero == placa_num) {
            placas[i].stuck = true;
            printf("Placa %d esta emperrada!\n", placas[i].numero);
            pthread_mutex_unlock(&lock);
            return;
        }
    }
    printf("Placa %d nao encontrada.\n", placa_num);

    pthread_mutex_unlock(&lock);
}

void limpar_tudo() {
    pthread_mutex_lock(&lock);
    
    contador = 0;
    printf("Tudo limpo.\n");
    
    pthread_mutex_unlock(&lock);
}

void *exit_thread(void *arg) {
    saida(tempo_saida);
    return NULL;
}

int main() {
    char command[20];
    pthread_t thread_id;

    pthread_mutex_init(&lock, NULL);

    printf("Bem-vindo ao Forno de Placas!\n");
    printf("Digite o tempo de saida (s): ");
    scanf("%d", &tempo_saida);
    getchar();

    pthread_create(&thread_id, NULL, exit_thread, NULL);

    while (1) {
        printf("Comandos: a (adicionar placa), s (simular emperramento), l (limpar tudo), q (sair)\n");
        printf("Digite um comando: ");
        scanf("%s", command);

        if (strcmp(command, "a") == 0) {
            adicionar_placa(tempo_saida);
        } else if (strcmp(command, "s") == 0) {
            int placa_num;
            printf("Digite o numero da placa para simular emperramento: ");
            scanf("%d", &placa_num);
            simular_emperramento(placa_num);
        } else if (strcmp(command, "l") == 0) {
            limpar_tudo();
        } else if (strcmp(command, "q") == 0) {
            running = false;
            break;
        } else {
            printf("Comando invalido.\n");
        }
    }
    pthread_join(thread_id, NULL);
    pthread_mutex_destroy(&lock);
    return 1;
}