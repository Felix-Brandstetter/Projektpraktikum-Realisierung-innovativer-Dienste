# Debian 11 aka Bullseye
FROM python:3.11-slim

#ARG TESSERACT_VERSION="main"
ARG TESSERACT_VERSION="5.3.1"
ARG TESSERACT_URL="https://api.github.com/repos/tesseract-ocr/tesseract/tarball/$TESSERACT_VERSION"
ARG imagemagic_config=/etc/ImageMagick-6/policy.xml


#Update
RUN apt-get update && apt-get --no-install-recommends --yes upgrade && apt upgrade && apt --no-install-recommends --yes upgrade

#Install imagemagick
RUN apt-get install --no-install-recommends --yes ghostscript imagemagick
#Allow Imagemagick to convert PDF
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="read|write" pattern="PDF" \/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi


#OpenCV dependencies
RUN apt-get install --no-install-recommends --yes ffmpeg libsm6 libxext6  -y

#Tesseract: install basic tools / dependencies of tesseract
RUN apt-get install --no-install-recommends --yes \
    apt-transport-https \
    asciidoc \
    automake \
    bash \
    ca-certificates \
    curl \
    docbook-xsl \
    g++ \
    git \
    libleptonica-dev \
    libtool \
    libicu-dev \
    libpango1.0-dev \
    libcairo2-dev \
    make \
    pkg-config \
    wget \
    xsltproc \
    #remove /var/lib/apt/lists/* to shrink imagesize
    && rm -rf /var/lib/apt/lists/*


#Tesseract: install tesseract
WORKDIR /tmp
RUN wget -qO tesseract.tar.gz $TESSERACT_URL && \
    tar -xzf tesseract.tar.gz && \
    rm tesseract.tar.gz && \
    mv tesseract-* tesseract

WORKDIR /tmp/tesseract

RUN ./autogen.sh && \
    ./configure && \
    make && \
    make install && \
    ldconfig

#Tesseract: go to default traineddata directory and import Languages
WORKDIR /usr/local/share/tessdata/
#English
RUN wget -qO eng.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/eng.traineddata?raw=true && \
    #German
    wget -qO deu.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/deu.traineddata?raw=true && \
    #Chinese
    wget -qO chi_sim.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/chi_sim.traineddata?raw=true


# Install pip requirements
WORKDIR /RIDSS2023
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

#Copy Files
COPY . /RIDSS2023

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" myuser && chown -R myuser /RIDSS2023
USER myuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "src/main/main.py"]