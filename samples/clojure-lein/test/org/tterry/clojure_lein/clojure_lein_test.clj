(ns org.tterry.clojure-lein.clojure-lein-test
  (:require [clojure.test :refer :all]
            [org.tterry.clojure-lein.clojure-lein :as cl]))

(deftest test-do-thing
  (testing "Should do something"
    (is (= true (cl/do-thing)))))

(deftest test-do-nothing
  (testing "Shouldnt do anything"
    (is (= false (cl/do-thing)))))