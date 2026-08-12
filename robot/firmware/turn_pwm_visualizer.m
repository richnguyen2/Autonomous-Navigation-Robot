kp_val = [1, 2, 4];

figure;
hold on;

for i = 1:length(kp_val)
    kp = kp_val(i);
    filename = sprintf("p_turn_data/turn_data_kp%d.csv", kp);
    data = readtable(filename);

    % Time Splice
    idx = data.time >= 0;

    % Response
    heading = data.pwm_val;

    plot(data.time(idx), heading(idx), 'LineWidth', 1.5, ...
        'DisplayName', sprintf("Kp = %d", kp));
end

% Baseline
data0 = readtable("p_turn_data/turn_data_base.csv");
plot(data0.time, data0.pwm_val, 'LineWidth', 1.5, ...
    'DisplayName', "Baseline");

% OS Kp = 1
dataOS = readtable("p_turn_data/turn_data_kp1_OS.csv");
plot(dataOS.time, dataOS.pwm_val, 'LineWidth', 1.5, ...
    'DisplayName', "Kp = 1, underdamp");


xlabel("Time (ms)");
ylabel("PWM (voltage)");
xlim([100, 500])
ylim([30, 80]);
title("PWM for Different Kp Values (Turn)");
legend("show")
grid on;
hold off;