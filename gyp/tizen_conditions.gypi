{
  'conditions': [
    ['building_for_tizen==1', {
      # Each tizen profile has its own cpu-specific flag.
      'cflags!': [
        '-march=armv7-a',
      ],
    }],
  ],
}
