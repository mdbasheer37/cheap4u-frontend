package org.cheap4u.helpers;

import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Context;
import android.hardware.fingerprint.FingerprintManager;
import android.os.Build;
import android.os.CancellationSignal;

/**
 * Fingerprint unlock helper for the Kivy/pyjnius app.
 *
 * Why this exists: the Python code used to call
 * androidx.core...FingerprintManagerCompat, which Google REMOVED in
 * androidx.core 1.13, and whose AuthenticationCallback is an abstract class
 * that pyjnius cannot implement from Python. This helper talks to the
 * platform FingerprintManager directly (no androidx) and reports back through
 * a plain interface, which pyjnius CAN implement.
 */
@SuppressWarnings("deprecation")
public class BiometricHelper {

    /** code: 0 = fingerprint recognised, 1 = not recognised (can try again), 2 = error / stopped */
    public interface Callback {
        void onResult(int code, String message);
    }

    private static CancellationSignal cancelSignal;

    /** True when the phone has a fingerprint sensor AND at least one enrolled fingerprint. */
    public static boolean isAvailable(Activity activity) {
        if (Build.VERSION.SDK_INT < 23) {
            return false;
        }
        try {
            return check(activity);
        } catch (Throwable t) {
            return false;
        }
    }

    @TargetApi(23)
    private static boolean check(Activity activity) {
        FingerprintManager fm =
                (FingerprintManager) activity.getSystemService(Context.FINGERPRINT_SERVICE);
        return fm != null && fm.isHardwareDetected() && fm.hasEnrolledFingerprints();
    }

    /** Start listening for a fingerprint. Results arrive on the callback (main thread). */
    public static void authenticate(Activity activity, final Callback callback) {
        if (Build.VERSION.SDK_INT < 23) {
            callback.onResult(2, "Fingerprint needs Android 6.0 or newer");
            return;
        }
        try {
            start(activity, callback);
        } catch (Throwable t) {
            callback.onResult(2, "Fingerprint unavailable: " + t);
        }
    }

    @TargetApi(23)
    private static void start(Activity activity, final Callback callback) {
        FingerprintManager fm =
                (FingerprintManager) activity.getSystemService(Context.FINGERPRINT_SERVICE);
        if (fm == null || !fm.isHardwareDetected() || !fm.hasEnrolledFingerprints()) {
            callback.onResult(2, "No fingerprint set up on this phone");
            return;
        }
        cancel();
        cancelSignal = new CancellationSignal();
        fm.authenticate(null, cancelSignal, 0, new FingerprintManager.AuthenticationCallback() {
            @Override
            public void onAuthenticationError(int errorCode, CharSequence errString) {
                if (errorCode == FingerprintManager.FINGERPRINT_ERROR_CANCELED) {
                    return; // we cancelled it ourselves - nothing to tell the user
                }
                callback.onResult(2, String.valueOf(errString));
            }

            @Override
            public void onAuthenticationFailed() {
                callback.onResult(1, "");
            }

            @Override
            public void onAuthenticationSucceeded(FingerprintManager.AuthenticationResult result) {
                callback.onResult(0, "");
            }
        }, null);
    }

    /** Stop listening (safe to call any time). */
    public static void cancel() {
        try {
            if (cancelSignal != null) {
                cancelSignal.cancel();
            }
        } catch (Throwable ignored) {
            // nothing to do
        }
        cancelSignal = null;
    }
}
