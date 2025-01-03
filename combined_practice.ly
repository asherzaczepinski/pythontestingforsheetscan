
\version "2.24.4"  % Force LilyPond to treat code with this version

\header {
    title = "Practice Scales"
    composer = "Traditional"
}

\paper {
    top-margin = 1.5\cm
    bottom-margin = 1.5\cm
    left-margin = 2\cm
    right-margin = 2\cm
    indent = 0
    system-count = #0
    line-width = 16\cm  % Adjust as needed
}


\markup \column {
  \center-column {
    \bold "C Major Scale"
  }
}

\score {
  \new Staff {
    % Force all accidentals to show (for any sharp or flat).
    \override Accidental #'force-accidental = ##t

    \relative c' {
      \time 4/4

      c4 d4 e4 f4 g4 a4 b4 c4 d4 e4 f4 g4 a4 b4 c4 b4 a4 g4 f4 e4 d4 c4 b4 a4 g4 f4 e4 d4 c4
    }
  }
  \layout {
    indent = 0
    ragged-right = ##t
  }
  \midi { }
}


\markup \column {
  \center-column {
    \bold "A Minor Scale"
  }
}

\score {
  \new Staff {
    % Force all accidentals to show (for any sharp or flat).
    \override Accidental #'force-accidental = ##t

    \relative a' {
      \time 4/4

      a4 b4 c4 d4 e4 f4 g4 a4 b4 c4 d4 e4 f4 g4 a4 g4 f4 e4 d4 c4 b4 a4 g4 f4 e4 d4 c4 b4 a4
    }
  }
  \layout {
    indent = 0
    ragged-right = ##t
  }
  \midi { }
}

