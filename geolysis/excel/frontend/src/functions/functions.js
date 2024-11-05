/* global uscs, aashto */

/**
 * AASHTO Classification System
 * @customfunction AASHTO
 * @param {number} liquidLimit Water content beyond which soils flows under their own weight.
 * @param {number} plasticityIndex Range of water content over which soil remains in plastic
 *                                 condition
 * @param {number} fines Percentage of fines in soil sample
 * @param {boolean} addGroupIndex Indicates whether the group index should be added to the soil
 *                                classification or not.
 * @returns {string} AASHTO classification of the soil.
 *
 */
export async function aashtoClassification(liquidLimit, plasticityIndex, fines, addGroupIndex = true) {
  try {
    const params = new URLSearchParams({
      liquidLimit,
      plasticityIndex,
      fines,
      addGroupIndex,
    });
    const url = `http://localhost:8000/aashto/?${params.toString()}`;

    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(response.statusText);
    }
    const jsonResponse = await response.json();
    return jsonResponse.classification;
  } catch (error) {
    return error;
  }
}

/**
 * USCS Classification System
 * @customfunction USCS
 * @param {number} liquidLimit Water content beyond which soils flows under their own weight.
 * @param {number} plasticLimit Water content at which plastic deformation can be initiated.
 * @param {number} fines Percentage of fines in soil sample
 * @param {number} sand Percentage of sand in soil sample
 * @param {number} d_10 Diameter at which 10% of the soil by weight is finer
 * @param {number} d_30 Diameter at which 30% of the soil by weight is finer
 * @param {number} d_60 Diameter at which 60% of the soil by weight is finer
 * @param {boolean} organic Indicates whether soil is organic or not
 * @returns {string} USCS classification of the soil.
 *
 */
export async function uscsClassification(
  liquidLimit,
  plasticLimit,
  fines,
  sand,
  d_10 = 0,
  d_30 = 0,
  d_60 = 0,
  organic = false
) {
  try {
    const params = new URLSearchParams({
      liquidLimit,
      plasticLimit,
      fines,
      sand,
      d_10,
      d_30,
      d_60,
      organic,
    });
    const url = `http://localhost:8000/uscs/?${params.toString()}`;

    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(response.statusText);
    }
    const jsonResponse = await response.json();
    return jsonResponse.classification;
  } catch (error) {
    return error;
  }
}

// /**
//  * Displays the current time once a second
//  * @customfunction
//  * @param {CustomFunctions.StreamingInvocation<string>} invocation Custom function invocation
//  */
// export function clock(invocation) {
//   const timer = setInterval(() => {
//     const time = currentTime();
//     invocation.setResult(time);
//   }, 1000);

//   invocation.onCanceled = () => {
//     clearInterval(timer);
//   };
// }

// /**
//  * Returns the current time
//  * @returns {string} String with the current time formatted for the current locale.
//  */
// export function currentTime() {
//   return new Date().toLocaleTimeString();
// }

// /**
//  * Increments a value once a second.
//  * @customfunction
//  * @param {number} incrementBy Amount to increment
//  * @param {CustomFunctions.StreamingInvocation<number>} invocation
//  */
// export function increment(incrementBy, invocation) {
//   let result = 0;
//   const timer = setInterval(() => {
//     result += incrementBy;
//     invocation.setResult(result);
//   }, 1000);

//   invocation.onCanceled = () => {
//     clearInterval(timer);
//   };
// }

// /**
//  * Writes a message to console.log().
//  * @customfunction LOG
//  * @param {string} message String to write.
//  * @returns String to write.
//  */
// export function logMessage(message) {
//   console.log(message);

//   return message;
// }
