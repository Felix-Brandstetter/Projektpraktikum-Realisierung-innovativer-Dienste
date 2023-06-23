FROM ubuntu:22.04

ARG imagemagic_config=/usr/local/etc/ImageMagick-7/policy.xml
ENV LANG=C.UTF-8
ENV TZ=UTC
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

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
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    tesseract-ocr-deu \
    tesseract-ocr-eng \
    tesseract-ocr-fra \
    tesseract-ocr-por \
    tesseract-ocr-spa \
    tesseract-ocr-ara \
    tesseract-ocr-dan \
    tesseract-ocr-fin \
    tesseract-ocr-hin \
    tesseract-ocr-ita \
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
    ffmpeg

# Compile and install jbig2
# Needs libleptonica-dev, zlib1g-dev
RUN \
    mkdir jbig2 \
    && curl -L https://github.com/agl/jbig2enc/archive/ea6a40a.tar.gz | \
    tar xz -C jbig2 --strip-components=1 \
    && cd jbig2 \
    && ./autogen.sh && ./configure && make && make install \
    && cd .. \
    && rm -rf jbig2

# Install ImageMagick 7 manually
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
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="disk" value="16EiB"\/> -->/<policy domain="resource" name="disk" value="10GiB"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
#Allow Imagemagick to process very large Images (Pixel)
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="width" value="10KP"\/> -->/<policy domain="resource" name="width" value="100000KP"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="height" value="10KP"\/> -->/<policy domain="resource" name="height" value="100000KP"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="map" value="4GiB"\/> -->/<policy domain="resource" name="map" value="10GiB"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="area" value="100MP"\/> -->/<policy domain="resource" name="area" value="10000MP"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi

#Pip
RUN curl https://bootstrap.pypa.io/get-pip.py | python3


WORKDIR /RIDSS2023

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" myuser && chown -R myuser /RIDSS2023
USER myuser
RUN ls /usr/local/etc/ImageMagick-7/

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy Files
COPY . /RIDSS2023

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["python", "src/service.py"]
