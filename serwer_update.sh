#!/bin/bash

# Ścieżka do repozytorium (zakładam, że skrypt i repozytorium są w tym samym katalogu)
# REPO_PATH="$(dirname "$(realpath "$0")")"
LOG_FILE="$REPO_PATH/logfile.log"

# Funkcja aktualizująca repozytorium i sprawdzająca zmiany
check_for_updates() {
    # cd $REPO_PATH
    
    # Pobierz najnowsze zmiany z repozytorium
    git fetch
    
    # Sprawdź, czy są jakieś nowe zmiany
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})

    if [ $LOCAL != $REMOTE ]; then
        git pull
        echo "There was some new data" | tee -a $LOG_FILE
        ./start_compose.sh
    fi
}

# Uruchomienie skryptu w nieskończonej pętli
while true; do
    check_for_updates
    sleep 1800  # Czekaj godzinę przed następnym sprawdzeniem
done
