#!/bin/bash

echo "-----------------------------------------------------------------------------"
echo "|                   © Execution QLearner Bot for ... game                     |"
echo "| Author : Alexis EGEA                                                      |"
echo "-----------------------------------------------------------------------------"
echo

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
	PYTHON_CMD=python3
elif [[ "$OSTYPE" == "cygwin"* || "$OSTYPE" == "msys"* ]]; then
 	PYTHON_CMD=python
else
	echo "Unsupported OS '$OSTYPE'"
	exit 1
fi

cd src/

while true; do
    echo "For this project, you have 3 possibilities:"
    echo "  1. Play a game of ..."
    echo "  2. Play a random bot"
    echo "  3. Play q-learner-based bot"
    read -p $"Select a number: " user_choice
    
    case "$user_choice" in
        1)
            echo "You chose to play a game of ... (human)."
            echo
            $PYTHON_CMD -m launcher_human
            break
            ;;
        2)
            echo "You chose to play the random bot."
            $PYTHON_CMD -m launcher_random
            break
            ;;
        3)
            echo "You chose to play the q-learner-based bot."
            $PYTHON_CMD -m launcher_qLearner
            break
            ;;
        *)
            echo "Invalid choice. Please select 1, 2, or 3."
            ;;
    esac
done


cd ..

echo 
read -p "Press any key to close the terminal window"
