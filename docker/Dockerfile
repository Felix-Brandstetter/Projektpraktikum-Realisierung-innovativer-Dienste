FROM ubuntu:22.04

ARG imagemagic_config=/usr/local/etc/ImageMagick-7/policy.xml
ARG TESSERACT_VERSION="5.3.1"
ARG TESSERACT_URL="https://api.github.com/repos/tesseract-ocr/tesseract/tarball/$TESSERACT_VERSION"
ENV LANG=C.UTF-8
ENV TZ=UTC
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

#Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    libqpdf-dev \
    zlib1g \
    liblept5 \
    ghostscript \
    jbig2dec \
    img2pdf \
    libsm6 libxext6 libxrender-dev \
    pngquant \
    unpaper \
    python-is-python3 \
    libcairo2-dev \
    libtiff-dev \
    build-essential autoconf automake libtool \
    libleptonica-dev \
    zlib1g-dev \
    python3-dev \
    python3-distutils \
    libffi-dev \
    ca-certificates \
    curl \
    git \
    ffmpeg \
    wget

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


#Install Languages
WORKDIR /usr/local/share/tessdata/
#English
RUN wget -qO eng.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/eng.traineddata?raw=true && \
    #German
    wget -qO deu.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/deu.traineddata?raw=true && \
    #Chinese
    wget -qO chi_sim.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/chi_sim.traineddata?raw=true && \
    #Französisch
    wget -qO fra.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/fra.traineddata?raw=true && \
    #Italienisch
    wget -qO ita.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/ita.traineddata?raw=true && \
    #Portugisisch
    wget -qO por.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/por.traineddata?raw=true && \
    #Spanisch
    wget -qO spa.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/spa.traineddata?raw=true && \
    #Arabisch
    wget -qO ara.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/ara.traineddata?raw=true && \
    #Dänisch
    wget -qO dan.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/dan.traineddata?raw=true && \
    #Finnisch
    wget -qO fin.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/fin.traineddata?raw=true && \
    #Hindu
    wget -qO hin.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/hin.traineddata?raw=true

WORKDIR /root

# Install ImageMagick 7 
RUN \
    mkdir imagemagick \
    && curl -L https://imagemagick.org/download/ImageMagick.tar.gz | \
    tar xz -C imagemagick --strip-components=1 \
    && cd imagemagick \
    && ./configure \
    && make \
    && make install \
    && ldconfig /usr/local/lib \
    && cd .. \
    && rm -rf imagemagick


#Unpaper
RUN apt-get install --no-install-recommends --yes unpaper libtiff-tools netpbm -y \
    && rm -rf /var/lib/apt/lists/*

#Allow Imagemagick to convert PDF
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="coder" rights="none" pattern="MVG" \/> -->/<policy domain="coder" rights="read|write" pattern="PDF" \/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
#Allow Imagemagick to process very large files (MB)
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="disk" value="16EiB"\/> -->/<policy domain="resource" name="disk" value="30GB"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
#Allow Imagemagick to process very large Images (Pixel)
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="width" value="10KP"\/> -->/<policy domain="resource" name="width" value="1000000MP"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="height" value="10KP"\/> -->/<policy domain="resource" name="height" value="1000000MP"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
#RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="map" value="4GiB"\/> -->/<policy domain="resource" name="map" value="10GiB"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="area" value="100MP"\/> -->/<policy domain="resource" name="area" value="10MP"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi

#Pip
RUN curl https://bootstrap.pypa.io/get-pip.py | python3


WORKDIR /RIDSS2023

# Creates a non-root user with an explicit UID and adds permission to access the /RIDSS2023 folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" myuser && chown -R myuser /RIDSS2023
USER myuser
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy Files
COPY . /RIDSS2023

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["python", "src/service.py"]
