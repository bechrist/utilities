/* timer.cpp - Timer Setup */
#include <string>
#include <map>

#include <chrono>
#include <cmath>

#include <iostream>
#include <iomanip>

#include "timer.hpp"

/* Aggregate Statistic */
AggregateStatistic::AggregateStatistic() {
    count = 0;
    min = std::nan("");
    max = std::nan("");
    mean = std::nan("");
    M2 = std::nan("");
    variance = std::nan(""); 
}

AggregateStatistic::AggregateStatistic(double initVal) {
    count = 1;
    min = initVal;
    max = initVal;
    mean = initVal;
    M2 = 0;
    variance = std::nan("");
}

void AggregateStatistic::append(double newVal) {
    // Updates aggregate statics using Welford's algorithm
    count += 1;

    if (count == 1) {
        min = newVal;
        max = newVal;
        mean = newVal;
        M2 = 0;
        variance = std::nan("");

        return;
    } 

    min = std::min(min, newVal);
    max = std::max(max, newVal);

    double del1 = newVal - mean;
    mean += del1 / count;
    double del2 = newVal - mean;
    M2 += del1*del2;

    if (count < 2) {
        variance = std::nan("");
    } else {
        variance = M2/(count-1);
    }
}

std::ostream& operator <<(std::ostream& os, const AggregateStatistic& aggStat) {
    auto w = os.width();

    os << std::setw(0) << "[count: " << std::setw(w) << aggStat.count
        << ", min: " << std::setw(w) << aggStat.min
        << ", max: " << std::setw(w) << aggStat.max
        << ", mean: " << std::setw(w) << aggStat.mean
        << ", variance: " << std::setw(w+4) << std::scientific << aggStat.variance << "]" 
        << std::endl << std::fixed << std::setw(w);

    return os;
}

/* Timers */
// TimerInstrumentor
TimerInstrumentor::TimerInstrumentor(): currentSession(nullptr) {}

void TimerInstrumentor::begin_session(const std::string& name) {
    currentSession = new TimerSession{name};
}

void TimerInstrumentor::end_session() {
    delete currentSession;
    currentSession = nullptr;
    statistics.clear();
}

void TimerInstrumentor::append_time(const TimerResult& result) {
    auto it = statistics.find(result.name);
    if (it != statistics.end()) {
        (*it).second.append(result.dur);
    }
    else {
        AggregateStatistic timeStat(result.dur);
        statistics.emplace(result.name, timeStat);
    }
}

TimerInstrumentor& TimerInstrumentor::get() {
    static TimerInstrumentor instance;
    return instance;
}

std::ostream& operator <<(std::ostream& os, const TimerInstrumentor TI) {
    int w = os.width();
    os << std::setw(0) << TI.currentSession->name << "\n";
    for (auto const& scp: TI.statistics) {
        os << std::setw(0) << "    " << std::setw(22) << scp.first << ": " << std::setw(w) << scp.second; 
    }

    return os;
}

// InstrumentedScopeTimer
InstrumentedScopeTimer::InstrumentedScopeTimer(std::string name)
    : name(std::move(name)),
      start(std::chrono::high_resolution_clock::now()) { }

InstrumentedScopeTimer::~InstrumentedScopeTimer() {
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

    TimerInstrumentor::get().append_time({name, duration/(double) 1000});
}