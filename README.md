# MediLogix 🏥 – Historial Médico con Flask + PostgreSQL + Docker

Este proyecto gestiona pacientes y casos médicos usando Flask y una base de datos PostgreSQL contenida en Docker.

---

## 🚀 Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.10+ instalado localmente

---

## ⚙️ Configuración Inicial

1. **Clona el repositorio**

```bash
git clone https://github.com/tu_usuario/medilogix.git
cd medilogix

docker-compose exec flask python seed.py
