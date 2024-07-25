/* timer.cpp Header File */
#ifndef TIMER_HPP
#define TIMER_HPP

#include <string>
#include <map>

#include <chrono>

#include <ostream>

#define TIMER       
#ifdef TIMER
    #define TIME_FUNC   InstrumentedScopeTimer t(std::string(__func__)+"()")
#else
    #define TIME_FUNC   
#endif

struct AggregateStatistic {
    int count;
    double min;
    double max;
    double mean;
    double M2;
    double variance;

    AggregateStatistic();
    AggregateStatistic(double initVal);

    void append(double newVal);
    friend std::ostream& operator <<(std::ostream& os, const AggregateStatistic& as);
};

struct TimerResult {
    std::string name;
    double dur;
};

struct TimerSession {
    std::string name; 
};

class TimerInstrumentor {
    private:
        TimerSession* currentSession;
        std::map<std::string, AggregateStatistic> statistics;
    public:
        TimerInstrumentor();

        void begin_session(const std::string& name);
        void end_session();

        void append_time(const TimerResult& result);

        static TimerInstrumentor& get();

        friend std::ostream& operator <<(std::ostream& os, TimerInstrumentor TI);
};

class InstrumentedScopeTimer {
    private:
        std::string name;
        std::chrono::time_point<std::chrono::high_resolution_clock> start;
    public:
        InstrumentedScopeTimer(std::string name);
        ~InstrumentedScopeTimer();
};

#endif 