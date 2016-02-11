{
  'target_defaults': {
    'variables': {
      'use_x11': 0,
      'skia_clang_build': 0,
      'skia_egl': 1,
      'skia_skip_gui': 1,
      'skia_arch_type%': 'arm',
      'arm_version%': 7,
      'arm_neon%': 0,
    },
    'defines!': [
      'SK_SAMPLES_FOR_X',
      'SK_ARM_HAS_NEON',
      'SK_ARM_HAS_OPTIONAL_NEON',
      '__ARM_NEON__',
    ],
    'libraries!': [
      '-lX11',
    ],
  },
}
