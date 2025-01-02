\version "2.22.0"  % Specify the LilyPond version


\paper {
  top-margin = 1.5\cm
  bottom-margin = 1.5\cm
  left-margin = 2\cm
  right-margin = 2\cm
  indent = 0
  line-width = 16\cm  % Adjust line width as needed
}

\book {

  \score {
    \header {
      title = "Major Scale in C"
      composer = "Traditional"
    }
    
    \new Staff {
      \markup {
        \bold \center-align "Major Scale in C"
        \vspace #2  % Add some vertical space between title and staff
      }
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

  \score {
    \header {
      title = "Harmonic Minor Scale in C"
      composer = "Traditional"
    }
    
    \new Staff {
      \markup {
        \bold \center-align "Harmonic Minor Scale in C"
        \vspace #2  % Add some vertical space between title and staff
      }
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
}
