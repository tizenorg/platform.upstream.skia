Name:       skia
Summary:    This is skia library.
Version:    5.0.5
Release:    0
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

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

BuildRequires: expat-devel, python, python-xml
%ifarch armv7l
BuildRequires: python-accel-armv7l-cross-arm
%endif
%ifarch aarch64
BuildRequires: python-accel-aarch64-cross-aarch64
%endif

BuildRequires: binutils-gold
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

build/apply_patches.sh
trap 'build/apply_patches.sh -r' EXIT

%ifarch aarhc64
  export ADDITION_OPTION=" -finline-limit=64 -foptimize-sibling-calls -fno-unwind-tables -fno-exceptions -Os"
%endif
%ifarch %{arm}
  export ADDITION_OPTION=" -finline-limit=64 -foptimize-sibling-calls -fno-unwind-tables -fno-exceptions -Os -mthumb"
  export CFLAGS="$(echo $CFLAGS | sed 's/-mfpu=[a-zA-Z0-9-]*/-mfpu=neon/g')"
  export CXXFLAGS="$(echo $CXXFLAGS | sed 's/-mfpu=[a-zA-Z0-9-]*/-mfpu=neon/g')"
  export FFLAGS="$(echo $FFLAGS | sed 's/-mfpu=[a-zA-Z0-9-]*/-mfpu=neon/g')"
%endif
%ifarch %{arm} aarch64
  export CFLAGS="$CFLAGS $ADDITION_OPTION"
  export CXXFLAGS="$CXXFLAGS $ADDITION_OPTION"
  export FFLAGS="$FFLAGS $ADDITION_OPTION"

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

%global SKIA_INCLUDE %{_includedir}/chromium/third_party/skia
%global SKIA_LIB %{_libdir}/chromium/third_party/skia

#set build mode
%if 0%{?_debug_mode}
%global OUTPUT_FOLDER %{OUTPUT_BASE_FOLDER}/Debug
%else
%global OUTPUT_FOLDER %{OUTPUT_BASE_FOLDER}/Release
%endif

./gyp_skia.sh \
%if %{!?_enable_test:0}%{?_enable_test:1}
    -Denable_test=1 \
%else
    -Denable_test=0 \
%endif
%ifarch %{arm}
    -Dsupport_arm=1
%else
    -Dsupport_arm=0
%endif

./build/prebuild/ninja/ninja %{?_smp_mflags} -C%{OUTPUT_FOLDER}

%install

install -d %{buildroot}%{_libdir}/pkgconfig
install -d %{buildroot}%{SKIA_LIB}/skia
install -d %{buildroot}%{SKIA_INCLUDE}/animator
install -d %{buildroot}%{SKIA_INCLUDE}/c
install -d %{buildroot}%{SKIA_INCLUDE}/include/codec
install -d %{buildroot}%{SKIA_INCLUDE}/include/config
install -d %{buildroot}%{SKIA_INCLUDE}/include/core
install -d %{buildroot}%{SKIA_INCLUDE}/include/device/xps
install -d %{buildroot}%{SKIA_INCLUDE}/include/effects
install -d %{buildroot}%{SKIA_INCLUDE}/include/gpu/effects
install -d %{buildroot}%{SKIA_INCLUDE}/include/gpu/gl
install -d %{buildroot}%{SKIA_INCLUDE}/include/images
install -d %{buildroot}%{SKIA_INCLUDE}/include/pathops
install -d %{buildroot}%{SKIA_INCLUDE}/include/pipe
install -d %{buildroot}%{SKIA_INCLUDE}/include/ports
install -d %{buildroot}%{SKIA_INCLUDE}/include/private
install -d %{buildroot}%{SKIA_INCLUDE}/include/svg
install -d %{buildroot}%{SKIA_INCLUDE}/include/utils
install -d %{buildroot}%{SKIA_INCLUDE}/include/views
install -d %{buildroot}%{SKIA_INCLUDE}/include/xml
install -d %{buildroot}%{SKIA_INCLUDE}/src/core
install -m 0644 ./build/pkgconfig/skia.pc                   %{buildroot}%{_libdir}/pkgconfig/
install -m 0644 %{OUTPUT_FOLDER}/libetc1.a                  %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libpng_static.a            %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libskia_codec.a            %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libskia_core.a             %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libskia_effects.a          %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libskia_icuuc.a            %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libskia_images.a           %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libskia_opts.a             %{buildroot}%{SKIA_LIB}/
%ifarch %{arm}
install -m 0644 %{OUTPUT_FOLDER}/libskia_opts_neon.a        %{buildroot}%{SKIA_LIB}/
%endif
install -m 0644 %{OUTPUT_FOLDER}/libskia_pdf.a              %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libskia_ports.a            %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libskia_sfnt.a             %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libskia_sfntly.a           %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libskia_skgpu.a            %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libskia_utils.a            %{buildroot}%{SKIA_LIB}/
install -m 0644 %{OUTPUT_FOLDER}/libSkKTX.a                 %{buildroot}%{SKIA_LIB}/
install -m 0644 ./include/animator/*.h                      %{buildroot}%{SKIA_INCLUDE}/animator/
install -m 0644 ./include/c/*.h                             %{buildroot}%{SKIA_INCLUDE}/c/
install -m 0644 ./include/codec/*.h                         %{buildroot}%{SKIA_INCLUDE}/include/codec/
install -m 0644 ./include/config/*.h                        %{buildroot}%{SKIA_INCLUDE}/include/config/
install -m 0644 ./include/core/*.h                          %{buildroot}%{SKIA_INCLUDE}/include/core/
install -m 0644 ./include/device/xps/*.h                    %{buildroot}%{SKIA_INCLUDE}/include/device/xps
install -m 0644 ./include/effects/*.h                       %{buildroot}%{SKIA_INCLUDE}/include/effects/
install -m 0644 ./include/gpu/*.h                           %{buildroot}%{SKIA_INCLUDE}/include/gpu/
install -m 0644 ./include/gpu/effects/*.h                   %{buildroot}%{SKIA_INCLUDE}/include/gpu/effects/
install -m 0644 ./include/gpu/gl/*.h                        %{buildroot}%{SKIA_INCLUDE}/include/gpu/gl
install -m 0644 ./include/images/*.h                        %{buildroot}%{SKIA_INCLUDE}/include/images/
install -m 0644 ./include/pathops/*.h                       %{buildroot}%{SKIA_INCLUDE}/include/pathops/
install -m 0644 ./include/pipe/*.h                          %{buildroot}%{SKIA_INCLUDE}/include/pipe/
install -m 0644 ./include/ports/*.h                         %{buildroot}%{SKIA_INCLUDE}/include/ports/
install -m 0644 ./include/private/*.h                       %{buildroot}%{SKIA_INCLUDE}/include/private/
install -m 0644 ./include/svg/*.h                           %{buildroot}%{SKIA_INCLUDE}/include/svg/
install -m 0644 ./include/utils/*.h                         %{buildroot}%{SKIA_INCLUDE}/include/utils/
install -m 0644 ./include/views/*.h                         %{buildroot}%{SKIA_INCLUDE}/include/views/
install -m 0644 ./include/xml/*.h                           %{buildroot}%{SKIA_INCLUDE}/include/xml/
install -m 0644 ./src/core/*.h                              %{buildroot}%{SKIA_INCLUDE}/src/core/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files devel
%manifest ./build/manifest/skia.manifest
%{_libdir}/pkgconfig/skia.pc
%{SKIA_LIB}/lib*.a
%{SKIA_INCLUDE}
