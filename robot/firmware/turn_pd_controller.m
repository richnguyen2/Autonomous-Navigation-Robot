kd_val = [0, 15, 100];

figure;
hold on;

for i = 1:length(kd_val)
    kd = kd_val(i);
    filename = sprintf("pd_turn_data_d%d.csv", kd);
    data = readtable(filename);

    % Time Splice
    idx = data.time >= 0;

    % Response
    heading = data.current_response;

    plot(data.time(idx), heading(idx), 'LineWidth', 1.5, ...
        'DisplayName', sprintf("Kd = %d", kd));
end

% % Baseline
% data0 = readtable("turn_data_base.csv");
% plot(data0.time, data0.current_response, 'LineWidth', 1.5, ...
%     'DisplayName', "Baseline");
% 
% data0 = readtable("p_turn_data/turn_data_kp1.csv");
% plot(data0.time, data0.current_response, 'LineWidth', 1.5, ...
%     'DisplayName', "Baseline");


yline(90, '--', 'LineWidth', 1, 'DisplayName', "Target");

xlabel("Time (ms)");
ylabel("Heading (degrees)");
title("Heading Response for Different Kd Values (Turn)");
legend("show")
grid on;
hold off;