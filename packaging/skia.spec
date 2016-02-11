Name:       skia
Summary:    This is skia library.
Version:    5.0.5
Release:    0
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    skia.manifest

# Conditions for OBS build
# The OBS build does not support running script 'build_{target}.sh'.
# TODO: There is a bug regarding mismatched versions from repository.
#       So, the versions need to be considered as originally intended versions,
#       until those versions are fixed by platform team.
#       1) The value '2.3' of macro 'tizen' should be '2.4'.
#       2) The value '2.0' of macro 'tizen' should be '2.3'.
%if "%{tizen}" == "3.0"
%define chromium_efl_tizen_version 3.0
%endif
%if "%{tizen}" == "2.3" || "%{tizen}" == "2.4"
%define chromium_efl_tizen_version 2.4
%endif
%if "%{tizen}" == "2.0"
%define chromium_efl_tizen_version 2.3
%endif

%if %{!?TIZEN_PROFILE_TV:0}%{?TIZEN_PROFILE_TV:1} || "%{?profile}" == "tv"
%define chromium_efl_tizen_profile tv
%endif
%if "%{!?profile:0}%{?profile}" == "mobile"
%define chromium_efl_tizen_profile mobile
%endif
%if "%{!?profile:0}%{?profile}" == "wearable"
%define chromium_efl_tizen_profile wearable
%endif
%if "%{!?profile:0}%{?profile}" == "common"
%define chromium_efl_tizen_profile common
%endif
%if "%{!?profile:0}%{?profile}" == "ivi"
%define chromium_efl_tizen_profile ivi
%endif

BuildRequires: expat-devel, python, python-xml, git
%ifarch armv7l
BuildRequires: python-accel-armv7l-cross-arm
%endif
%ifarch aarch64
BuildRequires: python-accel-aarch64-cross-aarch64
%endif

BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(gles20)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(zlib)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
This is skialibrary.

%package devel
Summary:  skia library (Development)
Group:    System/Development
Requires: %{name} = %{version}-%{release}

%description devel
This is skia library.
%devel_desc

%prep
%setup -q

%build

if [ ! -d %{buildroot}/../../OTHER/ -a -f /opt/testing/bin/rpmlint ]; then
  mkdir -p %{buildroot}/../../OTHER/
fi

git submodule update --init
pushd third_party/externals/fontconf/src;             git reset --hard f16c3118; popd;
pushd third_party/externals/giflib;                   git reset --hard ab10e256; popd;
pushd third_party/externals/gyp;                      git reset --hard 08429da7; popd;
pushd third_party/externals/icu;                      git reset --hard ce41627e; popd;
pushd third_party/externals/jsoncpp;                  git reset --hard 7165f6ac; popd;
pushd third_party/externals/libjpeg-turbo;            git reset --hard e4e75037; popd;
pushd third_party/externals/libpng;                   git reset --hard 070a616b; popd;
pushd third_party/externals/libwebp;                  git reset --hard 37f04949; popd;
pushd third_party/externals/nanomsg;                  git reset --hard 0e74bcc8; popd;
pushd third_party/externals/sfntly;                   git reset --hard 1bdaae8f; popd;
pushd third_party/externals/yasm/source/patched-yasm; git reset --hard 4671120c; popd;

build/apply_patches.sh
trap 'build/apply_patches.sh -r' EXIT

%ifarch %{arm} aarch64
  export ADDITION_OPTION=" -finline-limit=64 -foptimize-sibling-calls -fno-unwind-tables -fno-exceptions -Os"

  export CFLAGS="$CFLAGS $ADDITION_OPTION"
  export CXXFLAGS="$CXXFLAGS $ADDITION_OPTION"
  export FFLAGS="$FFLAGS $ADDITION_OPTION"

  export CFLAGS="$(echo $CFLAGS | sed 's/-mfpu=[a-zA-Z0-9-]*/-mfpu=neon/g')"
  export CXXFLAGS="$(echo $CXXFLAGS | sed 's/-mfpu=[a-zA-Z0-9-]*/-mfpu=neon/g')"
  export FFLAGS="$(echo $FFLAGS | sed 's/-mfpu=[a-zA-Z0-9-]*/-mfpu=neon/g')"

  export CFLAGS="$(echo $CFLAGS | sed 's/-Werror=maybe-uninitialized//g')"
  export CXXFLAGS="$(echo $CXXFLAGS | sed 's/-Werror=maybe-uninitialized//g')"
  export FFLAGS="$(echo $FFLAGS | sed 's/-Werror=maybe-uninitialized//g')"
%else
  export CFLAGS="$(echo $CFLAGS | sed 's/-Wl,--as-needed//g')"
  export CXXFLAGS="$(echo $CXXFLAGS | sed 's/-Wl,--as-needed//g')"
%endif

export GYP_GENERATORS=ninja

%define OUTPUT_BASE_FOLDER out.tz_v%{chromium_efl_tizen_version}.%{chromium_efl_tizen_profile}.%{_repository}
export GYP_GENERATOR_OUTPUT=$PWD/%{OUTPUT_BASE_FOLDER}
export SKIA_GYP_OUTPUT_DIR=$PWD/%{OUTPUT_BASE_FOLDER}
export GYP_GENERATOR_FLAGS="output_dir=${GYP_GENERATOR_OUTPUT}"

#set build mode
%if 0%{?_debug_mode}
%global OUTPUT_FOLDER %{OUTPUT_BASE_FOLDER}/Debug
%else
%global OUTPUT_FOLDER %{OUTPUT_BASE_FOLDER}/Release
%endif

./gyp_skia.sh \
%if %{!?_enable_test:0}%{?_enable_test:1}
    -Denable_test=1
%else
    -Denable_test=0
%endif

%ifarch %{arm}
./build/prebuild/ninja/ninja.arm %{?_smp_mflags} -C%{OUTPUT_FOLDER}
%else
%ifarch aarch64
./build/prebuild/ninja/ninja.arm64 %{?_smp_mflags} -C%{OUTPUT_FOLDER}
%else
./build/prebuild/ninja/ninja %{?_smp_mflags} -C%{OUTPUT_FOLDER}
%endif
%endif

%install
install -d %{buildroot}%{_libdir}/pkgconfig
install -d %{buildroot}%{_libdir}/skia
install -m 0755 %{OUTPUT_FOLDER}/lib*.a %{buildroot}%{_libdir}/skia
install -m 0644 ./packaging/skia.pc %{buildroot}%{_libdir}/pkgconfig/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest packaging/skia.manifest
%{_libdir}/skia/lib*.a

%files devel
%manifest packaging/skia.manifest
%{_libdir}/skia/lib*.a
%{_libdir}/pkgconfig/skia.pc
