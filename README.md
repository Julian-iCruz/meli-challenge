# MP Sec Tech Challenge 👋

El challenge fue afrontado creando una aplicación que tiene la capacidad de generar gráficas y tablas de valor para interpretar y entender los datos que tiene el dataset esto con el fin de reducir los tiempos de los análisis exploratorios de datos que consumen un largo tiempo a la hora de crear un modelo sólido y escalable.

El siguiente es un instructivo para poder realizar el despliegue de la aplicación creada. El despliegue es esta, se puede realizar de dos maneras:

* [Docker](#docker)
* [Virtualenv](#virtualenv)

# **Docker**

En caso de no tener [Docker](https://www.docker.com/) puede dirigirse al [link oficial](https://www.docker.com/) para descargarlo dependiendo de su sistema operativo.

Esta es la forma de despliegue más sencilla, ya que solo se debe ejecutar el siguiente comando:

```bash
docker compose up -d
```

Se creará el contenedor de la aplicación y se instalarán todas las librerías necesarias para el funcionamiento de la misma.

Para poder entrar a la App debe ingresar en el navegador web lo siguiente:

```bash
localhost:7777
```

Con estos sencillos pasos tendrá acceso a la App desarrollada.

# **Virtualenv**

En caso de no tener instalado [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) dirijase a la [documentacion oficial](https://virtualenv.pypa.io/en/latest/installation.html) o ejecuté el siguiente comando:

```bash
pip3 install virtualenv
```

Verifique que el módulo se instaló correctamente con el siguiente comando:

```bash
virtualenv --version
```

Cree un entorno virtual para dar independencia de los módulos que tiene en local y los módulos que son necesarios para correr la App. Reemplace ***< name-env >*** por el nombre que le quiere dar a su entorno virtual.

```bash
virtualenv <name-env>
```

Para activar el entorno anteriormente creado ejecuté el siguiente comando. Reemplace ***< name-env >*** por el nombre del entorno virtual anteriormente creado.

> **Nota:** 
Si su sistema operativo es LINUX o MACOS:

```bash
source ./<name-env>/bin/activate
```

> **Nota:** 
Si su sistema operativo es WINDOWS:

```bash
<name-env>\Scripts\activate.bat
```

Una vez activado el entorno virtual debe instalar los módulos necesarios para la ejecución de la App. Para ello ejecute el siguiente comando:

```bash
pip install -r requirements.txt
```

El último paso es correr, poner a correr la aplicación, para ello puede ejecutar el siguiente comando:

```bash
streamlit run 🏠_Home.py --server.port 7000
```

Para poder entrar a la App debe ingresar en el navegador web lo siguiente:

```bash
localhost:7000
```
