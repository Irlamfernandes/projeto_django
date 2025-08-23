#!/bin/sh
echo "===================================================="
echo " 🚀 O servidor do Django foi iniciado com sucesso!"
echo "===================================================="
echo ""

# Rodar migrações antes de iniciar
python manage.py migrate

echo " 👉 Para acessar o projeto, abra este link no seu navegador:"
echo "     🔗 http://localhost:8000"
echo ""
echo " 👉 Para acessar a área de administração do Django:"
echo "     🔗 http://localhost:8000/admin"
echo ""
echo " 💡 Dica: pressione CTRL + C para encerrar o servidor."
echo "===================================================="
echo ""

# Inicia o Django
python manage.py runserver 0.0.0.0:8000
