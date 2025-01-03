
\version "2.22.0"  % Specify the LilyPond version

\header {
  title = "C Scales"
  composer = "Traditional"
}

\paper {
  top-margin = 1.5\cm
  bottom-margin = 1.5\cm
  left-margin = 2\cm
  right-margin = 2\cm
  indent = 0
  system-count = #0  % Allow multiple systems
  line-width = 16\cm  % Adjust line width as needed
}


\markup \column {
  \center-column {
    \bold "Major Scale in C"
  }
}

\score {
  \new Staff {
    \relative c' {
      \key c \major
      \time 4/4

      c4 d4 e4 f4 g4 a4 b4 c4 d4 e4 f4 g4 a4 b4 c4 b4 a4 g4 f4 e4 d4 c4 b4 a4 g4 f4 e4 d4 c4
    }
  }

  \layout {
    indent = 0  % Remove indentation to center the music
    ragged-right = ##t  % Allow ragged right margins
  }
  \midi { }
}


\markup \column {
  \center-column {
    \bold "Minor Scale in C"
  }
}

\score {
  \new Staff {
    \relative c' {
      \key c \minor
      \time 4/4

      c4 d4 d#4 f4 g4 g#4 a#4 c4 d4 d#4 f4 g4 g#4 a#4 c4 a#4 g#4 g4 f4 d#4 d4 c4 a#4 g#4 g4 f4 d#4 d4 c4
    }
  }

  \layout {
    indent = 0  % Remove indentation to center the music
    ragged-right = ##t  % Allow ragged right margins
  }
  \midi { }
}


\markup \column {
  \center-column {
    \bold "Harmonic Minor Scale in C"
  }
}

\score {
  \new Staff {
    \relative c' {
      \key c \minor
      \time 4/4

      c4 d4 d#4 f4 g4 g#4 b4 c4 d4 d#4 f4 g4 g#4 b4 c4 b4 g#4 g4 f4 d#4 d4 c4 b4 g#4 g4 f4 d#4 d4 c4
    }
  }

  \layout {
    indent = 0  % Remove indentation to center the music
    ragged-right = ##t  % Allow ragged right margins
  }
  \midi { }
}

