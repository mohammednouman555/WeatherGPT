"use strict";

/*
 * ============================================================
 * WeatherGPT Dashboard
 * ============================================================
 *
 * Frontend responsibilities:
 * 1. Backend health check
 * 2. User input
 * 3. Current weather
 * 4. Forecast risk
 * 5. Decision intelligence
 * 6. WeatherGPT AI explanation
 * 7. Conversational WeatherGPT chat
 *
 * IMPORTANT:
 * Weather/risk calculations remain in the backend.
 * AI API keys are never exposed here.
 */


/* ============================================================
   CONFIGURATION
   ============================================================ */

const API_BASE = "";

const ENDPOINTS = {
    health: "/health/",
    currentWeather: "/api/weather/current",
    hourlyWeather: "/api/weather/hourly",
    dailyWeather: "/api/weather/daily",
    forecastRisk: "/api/risk/forecast",
    explainWeather: "/api/chat/explain",
    chatMessage: "/api/chat/message"
};


/* ============================================================
   DOM HELPER
   ============================================================ */

const $ = (id) => document.getElementById(id);


/* ============================================================
   DOM ELEMENTS
   ============================================================ */

const elements = {

    // System
    statusDot: $("statusDot"),
    statusText: $("statusText"),

    // Inputs
    cityInput: $("cityInput"),
    activitySelect: $("activitySelect"),
    startTime: $("startTime"),
    endTime: $("endTime"),

    // Analyze
    analyzeButton: $("analyzeButton"),
    buttonText: $("buttonText"),
    buttonLoader: $("buttonLoader"),

    // General
    errorMessage: $("errorMessage"),
    loadingState: $("loadingState"),
    resultsContainer: $("resultsContainer"),

    // Location
    locationName: $("locationName"),
    locationDetails: $("locationDetails"),
    latitude: $("latitude"),
    longitude: $("longitude"),

    // Weather
    weatherSource: $("weatherSource"),
    currentCondition: $("currentCondition"),
    currentTemperature: $("currentTemperature"),
    feelsLike: $("feelsLike"),
    humidity: $("humidity"),
    windSpeed: $("windSpeed"),
    rainfall: $("rainfall"),
    visibility: $("visibility"),

    // Decision
    decisionCard: $("decisionCard"),
    riskLevel: $("riskLevel"),
    riskScore: $("riskScore"),
    riskTitle: $("riskTitle"),
    decisionTitle: $("decisionTitle"),
    decisionMessage: $("decisionMessage"),
    decisionPriority: $("decisionPriority"),
    decisionHazard: $("decisionHazard"),

    // Risk summary
    hoursAnalyzed: $("hoursAnalyzed"),
    averageRisk: $("averageRisk"),
    peakRisk: $("peakRisk"),
    riskTrend: $("riskTrend"),

    // Hourly risk
    peakHazardBadge: $("peakHazardBadge"),
    hourlyResultsBody: $("hourlyResultsBody"),

    // Explanation
    explanationCard: $("explanationCard"),
    explanationText: $("explanationText"),
    explanationLoading: $("explanationLoading"),
    explanationButton: $("explanationButton"),

    // Chat
    userNameInput: $("userNameInput"),
    chatMessageInput: $("chatMessageInput"),
    sendChatButton: $("sendChatButton"),
    clearChatButton: $("clearChatButton"),
    askWeatherGPTButton: $("askWeatherGPTButton"),
    chatLoadingState: $("chatLoadingState"),
    chatErrorMessage: $("chatErrorMessage"),
    chatResponse: $("chatResponse"),
    chatExplanation: $("chatExplanation"),
    conversationMessages: $("conversationMessages")
};


/* ============================================================
   APPLICATION STATE
   ============================================================ */

const state = {

    currentWeather: null,

    hourlyForecast: null,

    dailyForecast: null,

    riskData: null,

    explanation: null,

    analysisComplete: false,

    explanationGenerating: false,

    conversationId:
        localStorage.getItem(
            "weathergpt_conversation_id"
        ) || null,

    conversationMessages: [],

    userPreferences: loadUserPreferences()
};


/* ============================================================
   INITIALIZATION
   ============================================================ */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        setDefaultTimes();

        restoreUserPreferences();

        initializeEventListeners();

        checkHealth();

    }
);


/* ============================================================
   EVENT LISTENERS
   ============================================================ */

function initializeEventListeners() {

    /* Analyze button */

    elements.analyzeButton?.addEventListener(
        "click",
        analyzeWeather
    );


    /* City Enter */

    elements.cityInput?.addEventListener(
        "keydown",
        (event) => {

            if (event.key === "Enter") {

                event.preventDefault();

                analyzeWeather();

            }

        }
    );


    /* Explain button */

    elements.explanationButton?.addEventListener(
        "click",
        requestExplanation
    );


    /* Ask WeatherGPT button */

    elements.askWeatherGPTButton?.addEventListener(
        "click",
        requestExplanation
    );


    /* Send chat */

    elements.sendChatButton?.addEventListener(
        "click",
        (event) => {

            event.preventDefault();

            sendChatMessage();

        }
    );


    /* Chat Enter */

    elements.chatMessageInput?.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendChatMessage();

            }

        }
    );


    /* New conversation */

    elements.clearChatButton?.addEventListener(
        "click",
        (event) => {

            event.preventDefault();

            startNewConversation();

        }
    );


    /* Preferences */

    elements.userNameInput?.addEventListener(
        "change",
        saveUserPreferences
    );


    document
        .querySelectorAll(".preferred-activity")
        .forEach(
            (input) => {

                input.addEventListener(
                    "change",
                    saveUserPreferences
                );

            }
        );

}


/* ============================================================
   DEFAULT TIMES
   ============================================================ */

function setDefaultTimes() {

    if (
        !elements.startTime ||
        !elements.endTime
    ) {

        return;

    }

    const now = new Date();

    const start = new Date(now);

    start.setMinutes(
        0,
        0,
        0
    );

    const end = new Date(start);

    end.setHours(
        end.getHours() + 2
    );

    elements.startTime.value =
        toDateTimeLocalValue(start);

    elements.endTime.value =
        toDateTimeLocalValue(end);

}


/* ============================================================
   DATETIME LOCAL FORMAT
   ============================================================ */

function toDateTimeLocalValue(date) {

    const year =
        date.getFullYear();

    const month =
        String(
            date.getMonth() + 1
        ).padStart(
            2,
            "0"
        );

    const day =
        String(
            date.getDate()
        ).padStart(
            2,
            "0"
        );

    const hours =
        String(
            date.getHours()
        ).padStart(
            2,
            "0"
        );

    const minutes =
        String(
            date.getMinutes()
        ).padStart(
            2,
            "0"
        );

    return (
        `${year}-${month}-${day}` +
        `T${hours}:${minutes}`
    );

}


/* ============================================================
   HEALTH CHECK
   ============================================================ */

async function checkHealth() {

    try {

        const response =
            await fetch(
                `${API_BASE}${ENDPOINTS.health}`
            );

        if (!response.ok) {

            throw new Error(
                "Backend health check failed."
            );

        }

        setSystemStatus(
            true,
            "System online"
        );

    } catch (error) {

        console.error(
            "Health check error:",
            error
        );

        setSystemStatus(
            false,
            "Backend unavailable"
        );

    }

}


/* ============================================================
   SYSTEM STATUS
   ============================================================ */

function setSystemStatus(
    online,
    message
) {

    if (elements.statusDot) {

        elements.statusDot.classList.toggle(
            "online",
            online
        );

        elements.statusDot.classList.toggle(
            "offline",
            !online
        );

    }

    if (elements.statusText) {

        elements.statusText.textContent =
            message;

    }

}


/* ============================================================
   MAIN WEATHER ANALYSIS
   ============================================================ */

async function analyzeWeather() {

    clearError();

    const city =
        elements.cityInput
            ?.value
            ?.trim() || "";

    const activity =
        elements.activitySelect
            ?.value
            ?.trim() || "General";

    const startTime =
        elements.startTime
            ?.value || "";

    const endTime =
        elements.endTime
            ?.value || "";


    /* Validation */

    if (!city) {

        showError(
            "Please enter a city."
        );

        elements.cityInput?.focus();

        return;

    }


    if (
        !startTime ||
        !endTime
    ) {

        showError(
            "Please select both start and end times."
        );

        return;

    }


    const start =
        new Date(startTime);

    const end =
        new Date(endTime);


    if (
        Number.isNaN(
            start.getTime()
        ) ||
        Number.isNaN(
            end.getTime()
        )
    ) {

        showError(
            "Please enter valid forecast times."
        );

        return;

    }


    if (end < start) {

        showError(
            "End time must be after start time."
        );

        return;

    }


    saveUserPreferences();

    setLoading(true);


    try {

        /*
         * Request weather + risk + hourly
         * forecast concurrently.
         */

        const [
            currentWeather,
            riskData,
            hourlyForecast
        ] = await Promise.all([

            fetchCurrentWeather(
                city
            ),

            fetchForecastRisk(
                city,
                startTime,
                endTime,
                activity
            ),

            fetchHourlyWeather(
                city
            )

        ]);


        /* Save state */

        state.currentWeather =
            currentWeather;

        state.riskData =
            riskData;

        state.hourlyForecast =
            hourlyForecast;

        state.analysisComplete =
            true;

        state.explanation =
            null;


        /*
         * A new weather analysis starts
         * a fresh conversation.
         */

        state.conversationId =
            null;

        state.conversationMessages =
            [];

        localStorage.removeItem(
            "weathergpt_conversation_id"
        );


        /* Render */

        renderCurrentWeather(
            currentWeather
        );

        renderRiskResults(
            riskData
        );

        renderLocation(
            riskData.location
        );

        resetExplanation();

        renderConversationMessages();


        /* Show results */

        elements.resultsContainer
            ?.classList.remove(
                "hidden"
            );


        elements.resultsContainer
            ?.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });


    } catch (error) {

        console.error(
            "WeatherGPT analysis error:",
            error
        );

        showError(
            getFriendlyErrorMessage(
                error
            )
        );

    } finally {

        setLoading(false);

    }

}


/* ============================================================
   CURRENT WEATHER API
   ============================================================ */

async function fetchCurrentWeather(
    city
) {

    const params =
        new URLSearchParams({
            city
        });

    const response =
        await fetch(
            `${API_BASE}` +
            `${ENDPOINTS.currentWeather}` +
            `?${params.toString()}`
        );


    if (!response.ok) {

        throw new Error(
            await extractApiError(
                response,
                "Unable to fetch current weather."
            )
        );

    }


    return response.json();

}


/* ============================================================
   HOURLY WEATHER API
   ============================================================ */

async function fetchHourlyWeather(
    city
) {

    const params =
        new URLSearchParams({
            city
        });

    const response =
        await fetch(
            `${API_BASE}` +
            `${ENDPOINTS.hourlyWeather}` +
            `?${params.toString()}`
        );


    if (!response.ok) {

        throw new Error(
            await extractApiError(
                response,
                "Unable to fetch hourly forecast."
            )
        );

    }


    return response.json();

}


/* ============================================================
   FORECAST RISK API
   ============================================================ */

async function fetchForecastRisk(
    city,
    startTime,
    endTime,
    activity
) {

    const params =
        new URLSearchParams({
            city,
            start_time: startTime,
            end_time: endTime,
            activity:
                activity || "General"
        });


    const response =
        await fetch(
            `${API_BASE}` +
            `${ENDPOINTS.forecastRisk}` +
            `?${params.toString()}`
        );


    if (!response.ok) {

        throw new Error(
            await extractApiError(
                response,
                "Unable to calculate weather risk."
            )
        );

    }


    return response.json();

}


/* ============================================================
   CURRENT WEATHER RENDERING
   ============================================================ */

function renderCurrentWeather(
    data
) {

    if (!data) {

        return;

    }


    if (elements.currentCondition) {

        elements.currentCondition.textContent =
            getFirstValue(
                data,
                [
                    "weather_condition",
                    "condition",
                    "weather"
                ],
                "—"
            );

    }


    if (elements.currentTemperature) {

        elements.currentTemperature.textContent =
            formatNumber(
                getFirstValue(
                    data,
                    [
                        "temperature",
                        "temperature_c"
                    ],
                    null
                ),
                1
            );

    }


    if (elements.feelsLike) {

        elements.feelsLike.textContent =
            formatNumber(
                getFirstValue(
                    data,
                    [
                        "feels_like",
                        "feels_like_temperature"
                    ],
                    null
                ),
                1
            );

    }


    if (elements.humidity) {

        elements.humidity.textContent =
            formatNumber(
                getFirstValue(
                    data,
                    [
                        "humidity",
                        "relative_humidity"
                    ],
                    null
                ),
                0
            );

    }


    if (elements.windSpeed) {

        elements.windSpeed.textContent =
            formatNumber(
                getFirstValue(
                    data,
                    [
                        "wind_speed",
                        "wind_speed_kmh"
                    ],
                    null
                ),
                1
            );

    }


    if (elements.rainfall) {

        elements.rainfall.textContent =
            formatNumber(
                getFirstValue(
                    data,
                    [
                        "rainfall",
                        "rain",
                        "precipitation"
                    ],
                    null
                ),
                1
            );

    }


    if (elements.visibility) {

        elements.visibility.textContent =
            formatVisibility(
                getFirstValue(
                    data,
                    [
                        "visibility"
                    ],
                    null
                )
            );

    }


    if (elements.weatherSource) {

        elements.weatherSource.textContent =
            data.source ||
            "Live weather";

    }

}


/* ============================================================
   LOCATION
   ============================================================ */

function renderLocation(
    location
) {

    if (!location) {

        return;

    }


    if (elements.locationName) {

        elements.locationName.textContent =
            location.name ||
            "Unknown location";

    }


    const details = [
        location.district,
        location.state,
        location.country
    ].filter(Boolean);


    if (elements.locationDetails) {

        elements.locationDetails.textContent =
            details.length
                ? details.join(", ")
                : "Location details unavailable";

    }


    if (elements.latitude) {

        elements.latitude.textContent =
            formatNumber(
                location.latitude,
                4
            );

    }


    if (elements.longitude) {

        elements.longitude.textContent =
            formatNumber(
                location.longitude,
                4
            );

    }

}


/* ============================================================
   RISK RESULTS
   ============================================================ */

function renderRiskResults(
    data
) {

    if (
        !data ||
        !data.risk
    ) {

        throw new Error(
            "The risk service returned an invalid response."
        );

    }


    const risk =
        data.risk;

    const decision =
        data.decision || {};


    const score =
        Number(
            decision.risk_score ??
            risk.peak_risk ??
            0
        );


    const level =
        decision.risk_level ||
        risk.peak_risk_level ||
        "Unknown";


    /* Score */

    if (elements.riskScore) {

        elements.riskScore.textContent =
            formatNumber(
                score,
                1
            );

    }


    /* Level */

    if (elements.riskLevel) {

        elements.riskLevel.textContent =
            level;

        applyRiskClass(
            elements.riskLevel,
            level
        );

    }


    /* Risk title */

    if (elements.riskTitle) {

        elements.riskTitle.textContent =
            decision.title ||
            `${level} Weather Risk`;

    }


    /* Decision card */

    if (elements.decisionCard) {

        applyRiskClass(
            elements.decisionCard,
            level
        );

    }


    /* Recommendation */

    if (elements.decisionTitle) {

        elements.decisionTitle.textContent =
            decision.title ||
            "Weather Assessment";

    }


    if (elements.decisionMessage) {

        elements.decisionMessage.textContent =
            decision.message ||
            "No recommendation was returned.";

    }


    if (elements.decisionPriority) {

        elements.decisionPriority.textContent =
            decision.priority ||
            "—";

    }


    if (elements.decisionHazard) {

        elements.decisionHazard.textContent =
            decision.hazard ||
            risk.peak_hazard ||
            "None";

    }


    /* Risk window */

    if (elements.hoursAnalyzed) {

        elements.hoursAnalyzed.textContent =
            risk.hours_analyzed ??
            "—";

    }


    if (elements.averageRisk) {

        elements.averageRisk.textContent =
            formatNumber(
                risk.average_risk,
                1
            );

    }


    if (elements.peakRisk) {

        elements.peakRisk.textContent =
            formatNumber(
                risk.peak_risk,
                1
            );

    }


    if (elements.riskTrend) {

        elements.riskTrend.textContent =
            risk.risk_trend ||
            "—";

    }


    /* Peak hazard */

    const peakHazard =
        risk.peak_hazard ||
        "None";

    const peakHazardValue =
        formatNumber(
            risk.peak_hazard_value,
            1
        );


    if (elements.peakHazardBadge) {

        elements.peakHazardBadge.textContent =
            `Peak hazard: ${peakHazard} ` +
            `(${peakHazardValue})`;

    }


    /* Hourly */

    renderHourlyResults(
        risk.hourly_results || []
    );

}


/* ============================================================
   HOURLY TABLE
   ============================================================ */

function renderHourlyResults(
    results
) {

    if (
        !elements.hourlyResultsBody
    ) {

        return;

    }


    elements.hourlyResultsBody
        .replaceChildren();


    if (!results.length) {

        const row =
            document.createElement(
                "tr"
            );

        const cell =
            document.createElement(
                "td"
            );

        cell.colSpan = 9;

        cell.textContent =
            "No hourly risk results available.";

        row.appendChild(cell);

        elements.hourlyResultsBody
            .appendChild(row);

        return;

    }


    for (
        const item of results
    ) {

        const row =
            document.createElement(
                "tr"
            );


        appendCell(
            row,
            formatForecastTime(
                item.forecast_time
            )
        );


        const riskCell =
            appendCell(
                row,
                formatNumber(
                    item.overall_risk,
                    1
                )
            );

        riskCell.classList.add(
            "table-risk"
        );


        const levelCell =
            document.createElement(
                "td"
            );


        const levelBadge =
            document.createElement(
                "span"
            );

        levelBadge.className =
            "table-level";


        const level =
            item.risk_level ||
            "Unknown";


        levelBadge.textContent =
            level;


        applyRiskClass(
            levelBadge,
            level
        );


        levelCell.appendChild(
            levelBadge
        );

        row.appendChild(
            levelCell
        );


        appendCell(
            row,
            item.weather_condition ||
            "—"
        );


        appendCell(
            row,
            formatNumber(
                item.rain_risk,
                1
            )
        );


        appendCell(
            row,
            formatNumber(
                item.wind_risk,
                1
            )
        );


        appendCell(
            row,
            formatNumber(
                item.heat_risk,
                1
            )
        );


        appendCell(
            row,
            formatNumber(
                item.visibility_risk,
                1
            )
        );


        const hazardCell =
            appendCell(
                row,
                item.weather_hazard ||
                "None"
            );


        hazardCell.classList.add(
            "hazard-cell"
        );


        elements.hourlyResultsBody
            .appendChild(row);

    }

}


/* ============================================================
   TABLE CELL
   ============================================================ */

function appendCell(
    row,
    value
) {

    const cell =
        document.createElement(
            "td"
        );

    cell.textContent =
        value ?? "—";

    row.appendChild(cell);

    return cell;

}


/* ============================================================
   RISK CLASS
   ============================================================ */

function applyRiskClass(
    element,
    level
) {

    if (!element) {

        return;

    }


    element.classList.remove(
        "risk-low",
        "risk-moderate",
        "risk-high",
        "risk-severe"
    );


    const normalized =
        String(level || "")
            .trim()
            .toLowerCase();


    if (
        normalized === "low"
    ) {

        element.classList.add(
            "risk-low"
        );

    } else if (
        normalized === "moderate" ||
        normalized === "medium"
    ) {

        element.classList.add(
            "risk-moderate"
        );

    } else if (
        normalized === "high"
    ) {

        element.classList.add(
            "risk-high"
        );

    } else if (
        normalized === "severe" ||
        normalized === "extreme"
    ) {

        element.classList.add(
            "risk-severe"
        );

    }

}


/* ============================================================
   WEATHER NORMALIZATION
   ============================================================ */

function normalizeWeatherForChat(
    data
) {

    if (!data) {

        return {};

    }


    return {

        temperature:
            getFirstValue(
                data,
                [
                    "temperature",
                    "temperature_c"
                ],
                null
            ),

        feels_like:
            getFirstValue(
                data,
                [
                    "feels_like",
                    "feels_like_temperature"
                ],
                null
            ),

        humidity:
            getFirstValue(
                data,
                [
                    "humidity",
                    "relative_humidity"
                ],
                null
            ),

        wind_speed:
            getFirstValue(
                data,
                [
                    "wind_speed",
                    "wind_speed_kmh"
                ],
                null
            ),

        rainfall:
            getFirstValue(
                data,
                [
                    "rainfall",
                    "rain",
                    "precipitation"
                ],
                null
            ),

        visibility:
            getFirstValue(
                data,
                [
                    "visibility"
                ],
                null
            ),

        condition:
            getFirstValue(
                data,
                [
                    "weather_condition",
                    "condition",
                    "weather"
                ],
                "Unknown"
            )

    };

}


/* ============================================================
   EXPLANATION REQUEST
   ============================================================ */

async function requestExplanation() {

    clearError();

    if (
        !state.analysisComplete ||
        !state.currentWeather ||
        !state.riskData
    ) {

        showError(
            "Please analyze the weather first."
        );

        return;

    }


    if (
        state.explanationGenerating
    ) {

        return;

    }


    const city =
        elements.cityInput
            ?.value
            ?.trim() ||
        "Unknown";


    const activity =
        elements.activitySelect
            ?.value
            ?.trim() ||
        "General";


    const payload = {

        city,

        activity,

        weather:
            normalizeWeatherForChat(
                state.currentWeather
            ),

        hourly_forecast:
            state.hourlyForecast
                ?.forecasts ||
            [],

        risk:
            state.riskData?.risk ||
            {},

        decision:
            state.riskData?.decision ||
            {},

        preferences:
            state.userPreferences ||
            loadUserPreferences()

    };


    state.explanationGenerating =
        true;

    setExplanationLoading(
        true
    );


    try {

        const response =
            await fetch(
                `${API_BASE}${ENDPOINTS.explainWeather}`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"

                    },

                    body:
                        JSON.stringify(
                            payload
                        )

                }
            );


        if (!response.ok) {

            throw new Error(
                await extractApiError(
                    response,
                    "Unable to generate WeatherGPT explanation."
                )
            );

        }


        const data =
            await response.json();


        if (
            !data ||
            data.success !== true ||
            typeof data.explanation !== "string" ||
            !data.explanation.trim()
        ) {

            throw new Error(
                "WeatherGPT returned an invalid LLM response."
            );

        }


        state.explanation =
            data.explanation.trim();


        renderExplanation(
            state.explanation
        );


    } catch (error) {

        console.error(
            "WeatherGPT explanation error:",
            error
        );

        showError(
            getFriendlyErrorMessage(
                error
            )
        );

    } finally {

        state.explanationGenerating =
            false;

        setExplanationLoading(
            false
        );

    }

}


/* ============================================================
   BUILD CHAT PAYLOAD
   ============================================================ */

function buildChatPayload(
    message
) {

    const city =
        elements.cityInput
            ?.value
            ?.trim() ||
        "Unknown";


    const activity =
        elements.activitySelect
            ?.value
            ?.trim() ||
        "General";


    return {

        message,

        /*
         * IMPORTANT:
         * Send existing conversation ID for
         * follow-up questions.
         *
         * Send null for the first message.
         */

        conversation_id:
            state.conversationId ||
            null,

        city,

        activity,

        weather:
            normalizeWeatherForChat(
                state.currentWeather ||
                {}
            ),

        hourly_forecast:
            state.hourlyForecast
                ?.forecasts ||
            [],

        risk:
            state.riskData?.risk ||
            {},

        decision:
            state.riskData?.decision ||
            {},

        preferences:
            state.userPreferences ||
            loadUserPreferences()

    };

}


/* ============================================================
   SEND CHAT MESSAGE
   ============================================================ */

async function sendChatMessage(
    messageOverride = null
) {

    clearError();


    /*
     * Validate analysis.
     */

    if (
        !state.analysisComplete ||
        !state.currentWeather ||
        !state.riskData
    ) {

        showChatError(
            "Please analyze the weather first."
        );

        return;

    }


    /*
     * Get message.
     */

    const inputMessage =
        messageOverride ||
        elements.chatMessageInput
            ?.value
            ?.trim() ||
        "";


    if (!inputMessage) {

        showChatError(
            "Please enter a question for WeatherGPT."
        );

        elements.chatMessageInput?.focus();

        return;

    }


    /*
     * Prevent duplicate requests.
     */

    if (
        state.explanationGenerating
    ) {

        return;

    }


    /*
     * Save preferences.
     */

    saveUserPreferences();


    /*
     * Loading.
     */

    state.explanationGenerating =
        true;

    setChatLoading(true);


    /*
     * Immediately show user's message.
     */

    appendConversationMessage(
        "user",
        inputMessage
    );


    /*
     * Clear input.
     */

    if (elements.chatMessageInput) {

        elements.chatMessageInput.value =
            "";

    }


    try {

        console.log(
            "WeatherGPT chat request:",
            buildChatPayload(
                inputMessage
            )
        );


        const response =
            await fetch(
                `${API_BASE}${ENDPOINTS.chatMessage}`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"

                    },

                    body:
                        JSON.stringify(
                            buildChatPayload(
                                inputMessage
                            )
                        )

                }
            );


        /*
         * HTTP error.
         */

        if (!response.ok) {

            const error =
                await extractApiError(
                    response,
                    "Unable to contact WeatherGPT."
                );

            throw new Error(
                error
            );

        }


        /*
         * Parse JSON.
         */

        const data =
            await response.json();


        console.log(
            "WeatherGPT chat response:",
            data
        );


        /*
         * Validate backend response.
         */

        if (
            !data ||
            data.success !== true ||
            typeof data.reply !== "string" ||
            !data.reply.trim()
        ) {

            throw new Error(
                "WeatherGPT returned an invalid chat response."
            );

        }


        /*
         * SAVE CONVERSATION ID
         *
         * This is essential for follow-up
         * questions such as:
         *
         * "What about at 9 PM?"
         */

        if (
            data.conversation_id
        ) {

            state.conversationId =
                data.conversation_id;

            localStorage.setItem(
                "weathergpt_conversation_id",
                state.conversationId
            );

        }


        /*
         * Get actual AI reply.
         */

        const reply =
            data.reply.trim();


        /*
         * Add assistant message.
         */

        appendConversationMessage(
            "assistant",
            reply
        );


        /*
         * IMPORTANT:
         * Explicitly render reply into the
         * visible chat response area.
         */

        renderChatReply(
            reply
        );


        /*
         * Also update explanation area.
         */

        renderExplanation(
            reply
        );


    } catch (error) {

        console.error(
            "WeatherGPT chat error:",
            error
        );


        showChatError(
            getFriendlyErrorMessage(
                error
            )
        );


    } finally {

        state.explanationGenerating =
            false;

        setChatLoading(false);

    }

}


/* ============================================================
   RENDER CHAT REPLY
   ============================================================ */

function renderChatReply(
    reply
) {

    if (!reply) {

        return;

    }


    /*
     * Main chat explanation text.
     */

    if (
        elements.chatExplanation
    ) {

        elements.chatExplanation.textContent =
            reply;

        elements.chatExplanation
            .classList.remove(
                "hidden"
            );

    }


    /*
     * Main response container.
     */

    if (
        elements.chatResponse
    ) {

        elements.chatResponse
            .classList.remove(
                "hidden"
            );

    }


    /*
     * If conversationMessages exists,
     * make sure it is visible too.
     */

    if (
        elements.conversationMessages
    ) {

        elements.conversationMessages
            .classList.remove(
                "hidden"
            );

    }

}


/* ============================================================
   CONVERSATION MESSAGE
   ============================================================ */

function appendConversationMessage(
    role,
    content
) {

    state.conversationMessages.push({

        role,

        content

    });


    renderConversationMessages();

}


/* ============================================================
   RENDER CONVERSATION
   ============================================================ */

function renderConversationMessages() {

    if (
        !elements.conversationMessages
    ) {

        return;

    }


    elements.conversationMessages
        .replaceChildren();


    for (
        const message
        of state.conversationMessages
    ) {

        const wrapper =
            document.createElement(
                "div"
            );


        wrapper.className =
            `chat-message ${message.role}`;


        const label =
            document.createElement(
                "span"
            );


        label.className =
            "chat-message-label";


        label.textContent =
            message.role === "user"
                ? "You"
                : "WeatherGPT";


        const content =
            document.createElement(
                "div"
            );


        content.textContent =
            message.content;


        wrapper.appendChild(
            label
        );


        wrapper.appendChild(
            content
        );


        elements.conversationMessages
            .appendChild(
                wrapper
            );

    }


    elements.conversationMessages
        .scrollTop =
        elements.conversationMessages
            .scrollHeight;

}


/* ============================================================
   NEW CONVERSATION
   ============================================================ */

async function startNewConversation() {

    const id =
        state.conversationId;


    /*
     * Clear backend conversation.
     */

    if (id) {

        try {

            const response =
                await fetch(
                    `${API_BASE}` +
                    `/api/chat/conversation/` +
                    `${encodeURIComponent(id)}`,
                    {

                        method: "DELETE",

                        headers: {

                            "Accept":
                                "application/json"

                        }

                    }
                );


            if (!response.ok) {

                console.warn(
                    "Backend conversation deletion failed."
                );

            }

        } catch (error) {

            console.warn(
                "Unable to clear server conversation:",
                error
            );

        }

    }


    /*
     * Reset frontend state.
     */

    state.conversationId =
        null;

    state.conversationMessages =
        [];

    state.explanation =
        null;


    localStorage.removeItem(
        "weathergpt_conversation_id"
    );


    renderConversationMessages();

    resetExplanation();


    /*
     * Clear visible chat response.
     */

    if (
        elements.chatExplanation
    ) {

        elements.chatExplanation.textContent =
            "";

    }


    if (
        elements.chatResponse
    ) {

        elements.chatResponse
            .classList.add(
                "hidden"
            );

    }


    if (
        elements.chatMessageInput
    ) {

        elements.chatMessageInput.value =
            "";

        elements.chatMessageInput.focus();

    }


    clearChatError();

}


/* ============================================================
   EXPLANATION RENDERING
   ============================================================ */

function renderExplanation(
    explanation
) {

    if (
        !elements.explanationText
    ) {

        return;

    }


    elements.explanationText.textContent =
        explanation;


    if (
        elements.explanationCard
    ) {

        elements.explanationCard
            .classList.remove(
                "hidden"
            );

    }

}


/* ============================================================
   RESET EXPLANATION
   ============================================================ */

function resetExplanation() {

    state.explanation =
        null;


    if (
        elements.explanationText
    ) {

        elements.explanationText.textContent =
            "Analyze the weather to generate a WeatherGPT explanation.";

    }


    if (
        elements.explanationLoading
    ) {

        elements.explanationLoading
            .classList.add(
                "hidden"
            );

    }


    if (
        elements.explanationButton
    ) {

        elements.explanationButton.disabled =
            false;

        elements.explanationButton.textContent =
            "Explain with WeatherGPT";

    }

}


/* ============================================================
   EXPLANATION LOADING
   ============================================================ */

function setExplanationLoading(
    loading
) {

    if (
        elements.explanationLoading
    ) {

        elements.explanationLoading
            .classList.toggle(
                "hidden",
                !loading
            );

    }


    if (
        elements.explanationButton
    ) {

        elements.explanationButton.disabled =
            loading;


        elements.explanationButton.textContent =
            loading
                ? "WeatherGPT is thinking..."
                : "Explain with WeatherGPT";

    }

}


/* ============================================================
   CHAT LOADING
   ============================================================ */

function setChatLoading(
    loading
) {

    if (
        elements.chatLoadingState
    ) {

        elements.chatLoadingState
            .classList.toggle(
                "hidden",
                !loading
            );

    }


    if (
        elements.sendChatButton
    ) {

        elements.sendChatButton.disabled =
            loading;

    }


    if (
        elements.askWeatherGPTButton
    ) {

        elements.askWeatherGPTButton.disabled =
            loading;

    }


    /*
     * Optional visual state for button.
     */

    if (
        elements.sendChatButton
    ) {

        elements.sendChatButton.textContent =
            loading
                ? "Sending..."
                : "Send";

    }

}


/* ============================================================
   LOADING STATE
   ============================================================ */

function setLoading(
    loading
) {

    if (
        elements.analyzeButton
    ) {

        elements.analyzeButton.disabled =
            loading;

    }


    if (
        elements.buttonText
    ) {

        elements.buttonText.textContent =
            loading
                ? "Analyzing..."
                : "Analyze Weather Risk";

    }


    if (
        elements.buttonLoader
    ) {

        elements.buttonLoader
            .classList.toggle(
                "hidden",
                !loading
            );

    }


    if (
        elements.loadingState
    ) {

        elements.loadingState
            .classList.toggle(
                "hidden",
                !loading
            );

    }

}


/* ============================================================
   ERROR DISPLAY
   ============================================================ */

function showError(
    message
) {

    if (
        !elements.errorMessage
    ) {

        console.error(
            message
        );

        return;

    }


    elements.errorMessage.textContent =
        message;


    elements.errorMessage
        .classList.remove(
            "hidden"
        );

}


/* ============================================================
   CLEAR ERROR
   ============================================================ */

function clearError() {

    if (
        elements.errorMessage
    ) {

        elements.errorMessage
            .classList.add(
                "hidden"
            );

        elements.errorMessage.textContent =
            "";

    }


    clearChatError();

}


/* ============================================================
   CHAT ERROR
   ============================================================ */

function showChatError(
    message
) {

    console.error(
        "WeatherGPT chat:",
        message
    );


    /*
     * Prefer dedicated chat error.
     */

    if (
        elements.chatErrorMessage
    ) {

        elements.chatErrorMessage.textContent =
            message;

        elements.chatErrorMessage
            .classList.remove(
                "hidden"
            );

        return;

    }


    /*
     * Fallback to general error.
     */

    showError(
        message
    );

}


/* ============================================================
   CLEAR CHAT ERROR
   ============================================================ */

function clearChatError() {

    if (
        elements.chatErrorMessage
    ) {

        elements.chatErrorMessage
            .classList.add(
                "hidden"
            );

        elements.chatErrorMessage.textContent =
            "";

    }

}


/* ============================================================
   API ERROR EXTRACTION
   ============================================================ */

async function extractApiError(
    response,
    fallback
) {

    try {

        const data =
            await response.json();


        if (
            typeof data.detail ===
            "string"
        ) {

            return data.detail;

        }


        if (
            Array.isArray(
                data.detail
            )
        ) {

            return data.detail
                .map(
                    item =>
                        item.msg ||
                        "Validation error"
                )
                .join("; ");

        }


        if (
            typeof data.message ===
            "string"
        ) {

            return data.message;

        }


        if (
            typeof data.error ===
            "string"
        ) {

            return data.error;

        }

    } catch (_) {

        /* Ignore invalid JSON */

    }


    return (
        `${fallback} ` +
        `HTTP ${response.status}.`
    );

}


/* ============================================================
   FRIENDLY ERROR
   ============================================================ */

function getFriendlyErrorMessage(
    error
) {

    const message =
        error?.message || "";


    if (
        message
            .toLowerCase()
            .includes(
                "failed to fetch"
            )
    ) {

        return (
            "WeatherGPT could not connect " +
            "to the backend. Make sure the " +
            "FastAPI server is running."
        );

    }


    if (
        message
            .toLowerCase()
            .includes(
                "api key"
            )
    ) {

        return (
            "WeatherGPT could not authenticate " +
            "with the AI service. Check the " +
            "LLM API configuration in the backend."
        );

    }


    if (
        message
            .toLowerCase()
            .includes(
                "quota"
            ) ||
        message
            .toLowerCase()
            .includes(
                "rate limit"
            )
    ) {

        return (
            "The AI service is temporarily " +
            "unavailable because its usage limit " +
            "has been reached. Please try again later."
        );

    }


    if (
        message.includes("500")
    ) {

        return (
            "WeatherGPT encountered a server " +
            "error while processing the request."
        );

    }


    return (
        message ||
        "Unable to complete the weather analysis."
    );

}


/* ============================================================
   USER PREFERENCES
   ============================================================ */

function loadUserPreferences() {

    try {

        const saved =
            JSON.parse(
                localStorage.getItem(
                    "weathergpt_preferences"
                ) || "{}"
            );


        return {

            name:
                typeof saved.name ===
                "string"
                    ? saved.name
                    : "",

            preferred_activities:
                Array.isArray(
                    saved.preferred_activities
                )
                    ? saved.preferred_activities
                    : [],

            language:
                "en"

        };

    } catch (_) {

        return {

            name: "",

            preferred_activities: [],

            language: "en"

        };

    }

}


/* ============================================================
   SAVE USER PREFERENCES
   ============================================================ */

function saveUserPreferences() {

    const name =
        elements.userNameInput
            ?.value
            ?.trim() ||
        "";


    const preferredActivities =
        Array.from(
            document.querySelectorAll(
                ".preferred-activity:checked"
            )
        )
        .map(
            input =>
                input.value
        );


    state.userPreferences = {

        name,

        preferred_activities:
            preferredActivities,

        language:
            "en"

    };


    localStorage.setItem(
        "weathergpt_preferences",
        JSON.stringify(
            state.userPreferences
        )
    );

}


/* ============================================================
   RESTORE USER PREFERENCES
   ============================================================ */

function restoreUserPreferences() {

    const preferences =
        state.userPreferences ||
        loadUserPreferences();


    if (
        elements.userNameInput
    ) {

        elements.userNameInput.value =
            preferences.name ||
            "";

    }


    document
        .querySelectorAll(
            ".preferred-activity"
        )
        .forEach(
            (input) => {

                input.checked =
                    preferences
                        .preferred_activities
                        .includes(
                            input.value
                        );

            }
        );

}


/* ============================================================
   NUMBER FORMAT
   ============================================================ */

function formatNumber(
    value,
    decimals = 1
) {

    if (
        value === null ||
        value === undefined ||
        value === "" ||
        Number.isNaN(
            Number(value)
        )
    ) {

        return "—";

    }


    return Number(value)
        .toFixed(
            decimals
        );

}


/* ============================================================
   VISIBILITY FORMAT
   ============================================================ */

function formatVisibility(
    value
) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return "—";

    }


    const number =
        Number(value);


    if (
        Number.isNaN(number)
    ) {

        return "—";

    }


    /*
     * Open-Meteo returns visibility
     * in metres.
     */

    if (
        number > 100
    ) {

        return (
            number / 1000
        ).toFixed(1);

    }


    return number.toFixed(1);

}


/* ============================================================
   FORECAST TIME FORMAT
   ============================================================ */

function formatForecastTime(
    value
) {

    if (!value) {

        return "—";

    }


    const date =
        new Date(value);


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return String(value);

    }


    return date.toLocaleString(
        [],
        {

            month:
                "short",

            day:
                "numeric",

            hour:
                "2-digit",

            minute:
                "2-digit"

        }
    );

}


/* ============================================================
   GET FIRST VALUE
   ============================================================ */

function getFirstValue(
    object,
    keys,
    fallback
) {

    if (!object) {

        return fallback;

    }


    for (
        const key of keys
    ) {

        if (
            object[key] !==
                undefined &&
            object[key] !==
                null
        ) {

            return object[key];

        }

    }


    return fallback;

}