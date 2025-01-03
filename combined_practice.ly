
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
    \bold "Major Scale in F# (Major)"
  }
}

\score {
  \new Staff {
    % Force all accidentals to show using LilyPond's built-in accidental
    % (in addition to the text markup we added manually)
    \override Accidental.free-standing-accidental = ##t
    \override Accidental.force-accidental = ##t

    \relative fis' {
      \key fis \major
      \time 4/4

      fis4^\markup{\sharp} gis4^\markup{\sharp} ais4^\markup{\sharp} b4 cis4^\markup{\sharp} dis4^\markup{\sharp} f4 fis4^\markup{\sharp} gis4^\markup{\sharp} ais4^\markup{\sharp} b4 cis4^\markup{\sharp} dis4^\markup{\sharp} f4 fis4^\markup{\sharp} f4 dis4^\markup{\sharp} cis4^\markup{\sharp} b4 ais4^\markup{\sharp} gis4^\markup{\sharp} fis4^\markup{\sharp} f4 dis4^\markup{\sharp} cis4^\markup{\sharp} b4 ais4^\markup{\sharp} gis4^\markup{\sharp} fis4^\markup{\sharp}
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
    \bold "Minor Scale in D# (Minor)"
  }
}

\score {
  \new Staff {
    % Force all accidentals to show using LilyPond's built-in accidental
    % (in addition to the text markup we added manually)
    \override Accidental.free-standing-accidental = ##t
    \override Accidental.force-accidental = ##t

    \relative dis' {
      \key dis \minor
      \time 4/4

      dis4^\markup{\sharp} f4 fis4^\markup{\sharp} gis4^\markup{\sharp} ais4^\markup{\sharp} b4 cis4^\markup{\sharp} dis4^\markup{\sharp} f4 fis4^\markup{\sharp} gis4^\markup{\sharp} ais4^\markup{\sharp} b4 cis4^\markup{\sharp} dis4^\markup{\sharp} cis4^\markup{\sharp} b4 ais4^\markup{\sharp} gis4^\markup{\sharp} fis4^\markup{\sharp} f4 dis4^\markup{\sharp} cis4^\markup{\sharp} b4 ais4^\markup{\sharp} gis4^\markup{\sharp} fis4^\markup{\sharp} f4 dis4^\markup{\sharp}
    }
  }
  \layout {
    indent = 0
    ragged-right = ##t
  }
  \midi { }
}

