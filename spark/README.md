# SPARK SQL

## Installation (windows 64bit)

1. Install python 3.11.9

Download `python-3.11.9-amd64.exe` from https://www.python.org/downloads/release/python-3119/ and install python 3.11.9.

2. Install pyspark 3.5.7

Run the following command. Make sure to install pyspark with python 3.11.9.

```bash
pip install pyspark==3.5.7
```

3. Add a system variable `PYSPARK_PYTHON`

Add a system variable whose the key is `PYSPARK_PYTHON` and the value is `C:\Users\<user>\AppData\Local\Programs\Python\Python311\python.exe`.

4. Install jdk11

Download `jdk-11.0.28_windows-x64_bin` from https://www.oracle.com/fr/java/technologies/javase/jdk11-archive-downloads.html and execute it.

5. Add a system variable `JAVA_HOME`

Add a system variable whose the key is `JAVA_HOME` and the value is `C:\Program Files\Java\jdk-11`.

6. (Optional) Download `winutils.exe`

To avoid the warning message about `HADOOP_HOME`, download `winutils.exe` from `https://github.com/cdarlint/winutils` and place it in `C:\hadoop\bin\winutils.exe`.

7. (Optional) Add a system variable `HADOOP_HOME`

After downloading `winutils.exe`, add a system variable whose the key is `HADOOP_HOME` and the value is `C:\hadoop`.