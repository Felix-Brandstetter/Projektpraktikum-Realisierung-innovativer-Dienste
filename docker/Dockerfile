FROM ubuntu:22.04

ARG imagemagic_config=/etc/ImageMagick-6/policy.xml
ENV LANG=C.UTF-8
ENV TZ=UTC
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update && apt-get install -y --no-install-recommends \
  python3 \
  libqpdf-dev \
  zlib1g \
  liblept5

RUN apt-get install -y --no-install-recommends \
  build-essential autoconf automake libtool \
  libleptonica-dev \
  zlib1g-dev \
  python3-dev \
  python3-distutils \
  libffi-dev \
  ca-certificates \
  curl \
  git

RUN \
  curl https://bootstrap.pypa.io/get-pip.py | python3

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

# For Tesseract 5
RUN apt-get update && apt-get install -y --no-install-recommends \
  software-properties-common gpg-agent
RUN add-apt-repository -y ppa:alex-p/tesseract-ocr-devel

RUN apt-get update && apt-get install -y --no-install-recommends \
  ghostscript \
  imagemagick \
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
  python-is-python3\
  libcairo2-dev



#OpenCV dependencies
RUN apt-get install --no-install-recommends --yes ffmpeg libsm6 libxext6

#Unpaper
RUN apt-get install --no-install-recommends --yes unpaper libtiff-tools netpbm  -y \
  && rm -rf /var/lib/apt/lists/*


#Allow Imagemagick to convert PDF
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="read|write" pattern="PDF" \/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi
RUN if [ -f $imagemagic_config ] ; then sed -i 's/<policy domain="resource" name="disk" value="1GiB"\/>/<policy domain="resource" name="disk" value="10GiB"\/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi

WORKDIR /RIDSS2023

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" myuser && chown -R myuser /RIDSS2023
USER myuser

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

#Copy Files
COPY . /RIDSS2023


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["python", "src/service.py"]
