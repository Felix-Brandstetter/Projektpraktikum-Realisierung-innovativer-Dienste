# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

FROM ubuntu:22.04 as base

ARG imagemagic_config=/usr/local/etc/ImageMagick-7/policy.xml

ENV LANG=C.UTF-8
ENV TZ=UTC
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update && apt-get install -y --no-install-recommends \
  python3 \
  libqpdf-dev \
  zlib1g \
  liblept5

FROM base as builder

# Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential autoconf automake libtool \
  libleptonica-dev \
  zlib1g-dev \
  python3-dev \
  python3-distutils \
  libffi-dev \
  ca-certificates \
  curl \
  git \
  libcairo2-dev \
  pkg-config

# Get the latest pip (Ubuntu version doesn't support manylinux2010)
RUN \
  curl https://bootstrap.pypa.io/get-pip.py | python3

# Compile and install jbig2
RUN \
  mkdir jbig2 \
  && curl -L https://github.com/agl/jbig2enc/archive/ea6a40a.tar.gz | \
  tar xz -C jbig2 --strip-components=1 \
  && cd jbig2 \
  && ./autogen.sh && ./configure && make && make install \
  && cd .. \
  && rm -rf jbig2

# Compile and install imagemagick
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

#Allow Imagemagick to convert PDF
#RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="coder" rights="none" pattern="MVG" \/> -->/<policy domain="coder" rights="read|write" pattern="PDF" \/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
#Allow Imagemagick to process very large files (MB)
#RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="disk" value="16EiB"\/> -->/<policy domain="resource" name="disk" value="30GB"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
#Allow Imagemagick to process very large Images (Pixel)
#RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="width" value="10KP"\/> -->/<policy domain="resource" name="width" value="1000000MP"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
##RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="height" value="10KP"\/> -->/<policy domain="resource" name="height" value="1000000MP"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
#RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="map" value="4GiB"\/> -->/<policy domain="resource" name="map" value="10GiB"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
#RUN if [ -f $imagemagic_config ] ; then sed -i 's/<!-- <policy domain="resource" name="area" value="100MP"\/> -->/<policy domain="resource" name="area" value="10MP"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi


COPY . /RIDSS2023

WORKDIR /RIDSS2023

FROM base

# For Tesseract 5
RUN apt-get update && apt-get install -y --no-install-recommends \
  software-properties-common gpg-agent
RUN add-apt-repository -y ppa:alex-p/tesseract-ocr-devel

#Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  ghostscript \
  fonts-droid-fallback \
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
  tesseract-ocr-ita \
  tesseract-ocr-hin \
  tesseract-ocr-dan \
  tesseract-ocr-fin \
  tesseract-ocr-ara \
  unpaper \
  git \
  libsm6 \
  libxext6 \
  ffmpeg \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /RIDSS2023
#Copy binaries
COPY --from=builder /usr/local/lib/ /usr/local/lib/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
RUN ldconfig /usr/local/lib 

# Creates a non-root user with an explicit UID and adds permission to access the /RIDSS2023 folder
RUN adduser -u 5678 --disabled-password --gecos "" dockeruser && chown -R dockeruser /RIDSS2023
USER dockeruser
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

#Copy Imagemagick Config/Policy.xml
COPY --from=builder /usr/local/etc/ImageMagick-7/ /usr/local/etc/ImageMagick-7/

# Copy minimal project files to get the test suite.
COPY --from=builder /RIDSS2023/tests /RIDSS2023/tests
