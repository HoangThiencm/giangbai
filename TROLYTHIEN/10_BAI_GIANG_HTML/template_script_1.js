
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']],
        displayMath: [['$$', '$$'], ['\\[', '\\]']]
      },
      options: {
        renderActions: {
          addTexAttribute: [150,
            (doc) => {
              for (const math of doc.math) {
                if (math.typesetRoot) {
                  const delim = math.display ? '$$' : '$';
                  math.typesetRoot.setAttribute('data-tex', delim + math.math + delim);
                }
              }
            },
            (math, doc) => {
              if (math.typesetRoot) {
                const delim = math.display ? '$$' : '$';
                math.typesetRoot.setAttribute('data-tex', delim + math.math + delim);
              }
            }
          ]
        }
      },
      svg: { fontCache: 'global' }
    };
  