kp_val = [0, 15, 100];

figure;
hold on;

for i = 1:length(kp_val)
    kp = kp_val(i);
    filename = sprintf("pd_turn_data_d%d.csv", kp);
    data = readtable(filename);

    % Time Splice
    idx = data.time >= 0;

    % Response
    heading = data.pwm_val;

    plot(data.time(idx), heading(idx), 'LineWidth', 1.5, ...
        'DisplayName', sprintf("Kp = %d", kp));
end


xlabel("Time (ms)");
ylabel("PWM (voltage)");
ylim([30, 80]);
title("PWM for Different Kd Values (Turn)");
legend("show")
grid on;
hold off;