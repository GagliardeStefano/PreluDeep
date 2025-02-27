import os

from keras.src.saving.saving_lib import load_model
from classes.Modello import Modello
from functions.data_accuracy import compare_with_all_tests
from functions.data_exploration import filtered_data_composer_from_maestro, get_notes
from functions.data_generation import create_track, save_track
from functions.data_mining import extract_data_midi, save_notes
from functions.data_preprocessing import crea_X_y, load_X_y

import pygame


def filtra_da_maestro(compositore_da_maestro):

    compositore = compositore_da_maestro.replace('é', 'e')
    src_dir = "maestro-v3.0.0"
    dest_dir = f"dataset/midi/{compositore}"
    new_csv_file = "dataset/infoMidi.csv"
    filtered_data_composer_from_maestro(compositore, src_dir, dest_dir, new_csv_file)

def estrai_salva_note_accordi(compositore, split):
    notes = extract_data_midi(compositore, split)
    save_notes(compositore, split, notes)

def crea_finestre_scorrimento(compositore, split):
    #compositore = "Frederic_Chopin"
    #split = "train"

    notes = get_notes(compositore, split)
    crea_X_y(notes, compositore, split)

    X, y = load_X_y(compositore, split)
    print(X.shape)
    print(y.shape)

def allena_nuovo_modello(compositore):
    modello = Modello(compositore)

    struct_model_compiled = modello.crea_struttura()
    history, model_allenato = modello.allena_modello(struct_model_compiled)

    modello.save_model(model_allenato)
    modello.plot_training_validation_loss()

def riprendi_allenamento(compositore, initial_epoch):
    modello = Modello(compositore)
    modello.riprendi_allenamento(initial_epoch)  # l'epoca (esclusa) da cui riprendere l'allenamento sul numero di epoche massimo


def genera_traccia(compositore):

    model = load_model(f"modelli_allenati/{compositore}/{compositore}.keras")
    X, _ = load_X_y(compositore, "train")

    music, melody_midi = create_track(model, compositore, X)
    print(music)
    save_track(compositore, melody_midi)

def calcola_accuracy_valori(compositore):
    generated_folder = f"tracce_generate/{compositore}"
    test_folder = f"dataset/midi/{compositore}/test"

    avg_results, accuracy_percentage, all_results = compare_with_all_tests(generated_folder, test_folder)
    print("Resultato medio", avg_results)
    print("Accuracy Modello", accuracy_percentage)
    print("Tutti i risultati", all_results)

def avvia_traccia(numero):
    dir_traccia = f"tracce_generate/Frederic_Chopin"
    traccia = f"output_melody_{numero}.mid"
    traccia_scelta = dir_traccia + "/" + traccia

    print(f"Riproducendo la traccia {traccia}...")

    # Inizializza pygame mixer e carica il file MIDI
    pygame.mixer.init()
    pygame.mixer.music.load(traccia_scelta)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        comando = input("'s' per fermare la riproduzione: ").strip().lower()
        if comando == 's':
            pygame.mixer.music.stop()
            print("Traccia fermata.")
            break


if __name__ == '__main__':
    '''GENERAZIONE TRACCIA'''
    #genera_traccia("Frederic_Chopin")

    '''CALCOLO ACCURATEZZA'''
    # calcola_accuracy_valori("Frederic_Chopin")


    while True:
        print("\n\n0-> esci\n1-> genera una traccia\n2-> ascolta una traccia\n")

        scelta = input("scegli un'opzione:")

        match scelta:
            case "0":
                exit(0)
            case "1":
                genera_traccia("Frederic_Chopin")
            case "2":
                dir = "tracce_generate/Frederic_Chopin"
                numero = int(input(f"Scegli un numero tra 1 e {len(os.listdir(dir))}: "))
                avvia_traccia(numero)

            case _:
                exit(0)