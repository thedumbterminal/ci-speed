(defproject org.tterry/clojure-lein "1.0.0"
            :description "Sample unit test report"
            :dependencies [[org.clojure/clojure "1.11.0"]]
  :profiles {:dev {:dependencies [[eftest "0.5.9"]]}}
  :plugins [[lein-eftest "0.5.9"]]
  :eftest {:report eftest.report.junit/report
           :report-to-file "target/junit.xml"})

